import pytest
import yaml

from os.path import abspath
from workloads.read_workloads_parser import YamlWorkloadParser


@pytest.mark.parametrize(
    "input_file, expected_cluster_name",
    [
        ("../static/OCPCluster1.yml", "OCPCluster1"),
        ("../static/OCPCluster2.yml", "OCPCluster2"),
        ("../static/OCPCluster3.yml", "OCPCluster3"),
        ("../static/OCPCluster4.yml", "OCPCluster4"),
        ("../static/OCPCluster5.yml", "OCPCluster5"),
    ],
    ids=["Cluster1", "Cluster2", "Cluster3", "Cluster4", "Cluster5"],
)
def test_get_cluster_name(input_file, expected_cluster_name):
    parser = YamlWorkloadParser(path=abspath(input_file))
    workload = parser.parse()

    assert workload.cluster_name == expected_cluster_name


@pytest.mark.parametrize(
    "input_file, expected_cpu_count",
    [
        ("../static/OCPCluster1.yml", 3.0),
        ("../static/OCPCluster2.yml", 2.0),
        ("../static/OCPCluster3.yml", 11.0),
        ("../static/OCPCluster4.yml", 14.0),
        ("../static/OCPCluster5.yml", 8.0),
    ],
    ids=["Cluster1", "Cluster2", "Cluster3", "Cluster4", "Cluster5"],
)
def test_get_cpu_count(input_file, expected_cpu_count):
    parser = YamlWorkloadParser(path=abspath(input_file))
    workload = parser.parse()

    cpu_cores = workload.total_cpu_cores()

    assert cpu_cores == expected_cpu_count, "Unmatched CPU count"


@pytest.mark.parametrize(
    "input_file, expected_memory_gig",
    [
        ("../static/OCPCluster1.yml", 12.0),
        ("../static/OCPCluster2.yml", 2.0),
        ("../static/OCPCluster3.yml", 20.0),
        ("../static/OCPCluster4.yml", 16.0),
        ("../static/OCPCluster5.yml", 2.0),
    ],
    ids=["Cluster1", "Cluster2", "Cluster3", "Cluster4", "Cluster5"],
)
def test_get_mem_count(input_file, expected_memory_gig):
    parser = YamlWorkloadParser(path=abspath(input_file))
    workload = parser.parse()

    memory_gig = workload.total_memory_gig()

    assert memory_gig == expected_memory_gig, "Unmatched Memory count"


@pytest.mark.parametrize(
    "input_file, expected_nodes",
    [
        ("../static/OCPCluster1.yml", ["node1", "node2"]),
        ("../static/OCPCluster2.yml", ["node1B"]),
        ("../static/OCPCluster3.yml", ["node1C", "node2C"]),
        ("../static/OCPCluster4.yml", ["node1C", "node2C"]),
        ("../static/OCPCluster5.yml", ["node1E", "node2E"]),
    ],
    ids=["Cluster1", "Cluster2", "Cluster3", "Cluster4", "Cluster5"],
)
def test_get_all_nodes(input_file, expected_nodes):
    parser = YamlWorkloadParser(path=abspath(input_file))
    workload = parser.parse()

    assert sorted(workload.all_node_names()) == sorted(expected_nodes), "Unmatched node names"


@pytest.mark.parametrize(
    "input_file, expected_namespaces",
    [
        ("../static/OCPCluster1.yml", ["ns1", "ns2", "ns3"]),
        ("../static/OCPCluster2.yml", ["ns1"]),
        ("../static/OCPCluster3.yml", ["ns1", "ns2", "ns3", "ns4", "ns5"]),
        ("../static/OCPCluster4.yml", ["ns1", "ns2"]),
        ("../static/OCPCluster5.yml", ["ns1", "ns2", "ns3"]),
    ],
    ids=["Cluster1", "Cluster2", "Cluster3", "Cluster4", "Cluster5"],
)
def test_get_all_namespaces(input_file, expected_namespaces):
    parser = YamlWorkloadParser(path=abspath(input_file))
    workload = parser.parse()

    namespaces = workload.all_namespaces_names()

    assert sorted(namespaces) == sorted(expected_namespaces), "Unmatched ns names"


@pytest.mark.parametrize(
    "input_file, expected_pods",
    [
        ("../static/OCPCluster1.yml", ["pod_1", "pod_2", "pod_3"]),
        ("../static/OCPCluster2.yml", ["pod_1", "pod_2"]),
        (
                "../static/OCPCluster3.yml",
                [
                    "pod_1",
                    "pod_2",
                    "pod_3",
                    "pod_4",
                    "pod_2",
                    "pod_1",
                    "pod_2",
                    "pod_4",
                    "pod_1",
                    "pod_4",
                    "pod_2",
                ],
        ),
        ("../static/OCPCluster4.yml", ["pod_1", "pod_2"]),
        ("../static/OCPCluster5.yml", ["pod_1", "pod_2", "pod_3"]),
    ],
    ids=["Cluster1", "Cluster2", "Cluster3", "Cluster4", "Cluster5"],
)
def test_get_all_pods(input_file, expected_pods):
    parser = YamlWorkloadParser(path=abspath(input_file))
    workload = parser.parse()

    pods = workload.all_pod_names()

    assert sorted(pods) == sorted(expected_pods), "Unmatched pod names"


@pytest.mark.parametrize(
    "input_file, nodes_regex,expected_ns",
    [
        ("../static/OCPCluster1.yml", "node1", ["ns1", "ns2"]),
        ("../static/OCPCluster1.yml", "node2", ["ns3"]),
        ("../static/OCPCluster1.yml", "node", ["ns1", "ns2", "ns3"]),
        ("../static/OCPCluster1.yml", "fake:regex", []),
    ],
    ids=["node1", "node2", "node", "fake_regex"],
)
def test_get_ns_by_node(input_file, nodes_regex, expected_ns):
    parser = YamlWorkloadParser(path=abspath(input_file))
    workload = parser.parse()

    namespaces = workload.namespaces_by_partial_node_name(search=nodes_regex)
    assert sorted(namespaces) == sorted(expected_ns)


@pytest.mark.parametrize(
    "input_file,label,expected_label_values",
    [
        ("../static/OCPCluster1.yml", "ns_name", ("ns1")),
        ("../static/OCPCluster1.yml", "tier", ("pod_1", "pod_2", "pod_3")),
        ("../static/OCPCluster1.yml", "node_name", ("node1", "node2")),
        ("../static/OCPCluster1.yml", "ns_name", ("ns1", "ns2", "ns3")),
    ],
    ids=["node1", "node1", "node1", "node1"],
)
def test_get_cluster_labels(input_file, label, expected_label_values):
    raise NotImplemented("Pending to do")
