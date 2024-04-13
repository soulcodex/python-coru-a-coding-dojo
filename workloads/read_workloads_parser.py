from typing import Text, Dict, Any, List, Set
from workloads.read_workloads import Workload, Node, Namespace, Pod
from abc import ABC, abstractmethod

import yaml


class WorkloadParser(ABC):

    @abstractmethod
    def parse(self) -> Workload:
        pass


class YamlWorkloadParser(WorkloadParser):

    def __init__(self, path: Text):
        self.path = path

    def __get_file_content(self) -> Text:
        with open(self.path) as cluster_file:
            return cluster_file.read()

    def __get_namespace_pods(self, raw_pods: List[Dict[Text, Any]]) -> List[Pod]:
        pods = []

        if len(raw_pods) == 0:
            return pods

        for raw_pod in raw_pods:
            pod = Pod(name=raw_pod.get('pod_name'), labels=[])
            pods.append(pod)

        return pods

    def __get_node_namespaces(self, raw_namespaces: Dict[Text, Dict[Text, Any]]) -> List[Namespace]:
        namespaces = []

        if len(raw_namespaces.keys()) == 0:
            return []

        for namespace_name in raw_namespaces.keys():
            ns_pods = self.__get_namespace_pods(raw_namespaces.get(namespace_name, {}).get('pods', []))
            namespace = Namespace(name=namespace_name, pods=ns_pods, labels=[])
            namespaces.append(namespace)
        return namespaces

    def __get_cluster_nodes(self, raw_nodes: List[Dict[Text, Any]]) -> List[Node]:
        nodes = []

        if len(raw_nodes) == 0:
            return nodes

        for raw_node in raw_nodes:
            raw_node_labels: Text = raw_node.get('node_labels', '')
            node = Node(
                labels=raw_node_labels.split(sep='|'),
                name=raw_node.get('node_name'),
                cpu_cores=raw_node.get('cpu_cores'),
                memory_gig=raw_node.get('memory_gig'),
                namespaces=self.__get_node_namespaces(raw_node.get('namespaces', {}))
            )
            nodes.append(node)
        return nodes

    def parse(self) -> Workload:
        content = self.__get_file_content()
        content_as_yaml: Dict[Text, Any] = yaml.safe_load(content)['data'][0]
        cluster_info: Dict[Text, Any] = content_as_yaml.get('OCPCluster')
        return Workload(
            cluster_name=cluster_info.get('cluster_name'),
            nodes=self.__get_cluster_nodes(cluster_info.get('nodes'))
        )
