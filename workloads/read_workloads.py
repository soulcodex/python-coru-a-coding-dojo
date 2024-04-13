import regex as re
from typing import Text, List, Optional

Labels = List[Text]


class Pod:

    def __init__(self, name: Text, labels: Labels):
        self.name = name
        self.labels = labels


class Namespace:

    def __init__(self, name: Text, pods: List[Pod], labels: Labels):
        self.name = name
        self.pods = pods
        self.labels = labels

    def namespace_pod_names(self) -> List[Text]:
        return [pod.name for pod in self.pods]


class Node:

    def __init__(self, labels: Labels, name: Text, cpu_cores: int, memory_gig: int, namespaces: List[Namespace]):
        self.labels = labels
        self.name = name
        self.cpu_cores = cpu_cores
        self.memory_gig = memory_gig
        self.namespaces = namespaces

    def node_pod_names(self) -> List[Text]:
        pod_names = []
        for namespace in self.namespaces:
            pod_names.extend(namespace.namespace_pod_names())
        return pod_names

    def node_namespace_names(self) -> List[Text]:
        return [ns.name for ns in self.namespaces]

    def node_namespace_by_node_name(self, search: Text) -> List[Text]:
        matched_namespaces = []
        node_name_match: Optional[re.Match] = re.match(search, self.name)

        if isinstance(node_name_match, re.Match):
            matched_namespaces.extend([ns.name for ns in self.namespaces])

        return matched_namespaces


class Workload:

    def __init__(self, cluster_name: Text, nodes: List[Node]):
        self.cluster_name = cluster_name
        self.nodes = nodes

    def all_node_names(self) -> List[Text]:
        node_names = []
        for node in self.nodes:
            node_names.append(node.name)
        return node_names

    def all_namespaces_names(self) -> List[Text]:
        namespaces = []
        for node in self.nodes:
            namespaces.extend(node.node_namespace_names())
        return namespaces

    def all_pod_names(self) -> List[Text]:
        pod_names = []
        for node in self.nodes:
            pod_names.extend(node.node_pod_names())
        return pod_names

    def total_cpu_cores(self) -> float:
        total_cpu_cores = 0
        for node in self.nodes:
            total_cpu_cores += node.cpu_cores
        return total_cpu_cores

    def total_memory_gig(self) -> float:
        total_memory_gig = 0
        for node in self.nodes:
            total_memory_gig += node.memory_gig
        return total_memory_gig

    def namespaces_by_partial_node_name(self, search: Text) -> List[Text]:
        matched_namespaces = []
        for node in self.nodes:
            matched_namespaces.extend(node.node_namespace_by_node_name(search=search))
        return matched_namespaces
