from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException
from datetime import datetime, timezone

from models import ClusterSummary
import os

def load_config():
    try:
        config.load_incluster_config()
    except ConfigException:
        config.load_kube_config()


def get_cluster_summary():

    load_config()

    core = client.CoreV1Api()
    apps = client.AppsV1Api()

    # ----------------------
    # Report Information
    # ----------------------

    date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    try:
        contexts, active = config.list_kube_config_contexts()
        cluster_name = active["context"]["cluster"]
    except Exception:
        cluster_name = os.getenv("CLUSTER_NAME", "unknown")

    environment = "Dev"

    # ----------------------
    # Kubernetes Resources
    # ----------------------

    nodes = core.list_node().items
    namespaces = core.list_namespace().items
    pods = core.list_pod_for_all_namespaces().items

    deployments = apps.list_deployment_for_all_namespaces().items
    statefulsets = apps.list_stateful_set_for_all_namespaces().items
    daemonsets = apps.list_daemon_set_for_all_namespaces().items

    # ----------------------
    # Counters
    # ----------------------

    ready_nodes = 0

    running_pods = 0
    pending_pods = 0
    failed_pods = 0
    crashloop_pods = 0

    ready_deployments = 0
    ready_statefulsets = 0
    ready_daemonsets = 0

    # ----------------------
    # Nodes
    # ----------------------

    for node in nodes:

        for condition in node.status.conditions:

            if condition.type == "Ready" and condition.status == "True":
                ready_nodes += 1

    # ----------------------
    # Pods
    # ----------------------

    for pod in pods:

        if pod.status.phase == "Running":
            running_pods += 1

        elif pod.status.phase == "Pending":
            pending_pods += 1

        elif pod.status.phase == "Failed":
            failed_pods += 1

        for status in pod.status.container_statuses or []:

            waiting = status.state.waiting

            if waiting and waiting.reason == "CrashLoopBackOff":
                crashloop_pods += 1

    # ----------------------
    # Deployments
    # ----------------------

    for deployment in deployments:

        desired = deployment.spec.replicas or 0
        ready = deployment.status.ready_replicas or 0

        if desired == ready:
            ready_deployments += 1

    # ----------------------
    # StatefulSets
    # ----------------------

    for sts in statefulsets:

        desired = sts.spec.replicas or 0
        ready = sts.status.ready_replicas or 0

        if desired == ready:
            ready_statefulsets += 1

    # ----------------------
    # DaemonSets
    # ----------------------

    for ds in daemonsets:

        desired = ds.status.desired_number_scheduled or 0
        ready = ds.status.number_ready or 0

        if desired == ready:
            ready_daemonsets += 1

    cluster_healthy = (
        ready_nodes == len(nodes)
        and pending_pods == 0
        and failed_pods == 0
        and crashloop_pods == 0
    )

    return ClusterSummary(
        date=date,
        cluster_name=cluster_name,
        environment=environment,

        ready_nodes=ready_nodes,
        total_nodes=len(nodes),

        namespaces=len(namespaces),

        running_pods=running_pods,
        pending_pods=pending_pods,
        failed_pods=failed_pods,
        crashloop_pods=crashloop_pods,

        ready_deployments=ready_deployments,
        total_deployments=len(deployments),

        ready_statefulsets=ready_statefulsets,
        total_statefulsets=len(statefulsets),

        ready_daemonsets=ready_daemonsets,
        total_daemonsets=len(daemonsets),

        cluster_healthy=cluster_healthy,
    )