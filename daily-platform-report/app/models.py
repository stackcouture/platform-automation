from dataclasses import dataclass


@dataclass
class ClusterSummary:

    # Report Information
    date: str
    cluster_name: str
    environment: str

    # Cluster Health
    ready_nodes: int
    total_nodes: int

    namespaces: int

    running_pods: int
    pending_pods: int
    failed_pods: int
    crashloop_pods: int

    # Workload Status
    ready_deployments: int
    total_deployments: int

    ready_statefulsets: int
    total_statefulsets: int

    ready_daemonsets: int
    total_daemonsets: int

    cluster_healthy: bool