from models import ClusterSummary

def generate(summary: ClusterSummary) -> str:

    report = f"""
==================================================
Daily Platform Report
==================================================

Date        : {summary.date}
Cluster     : {summary.cluster_name}
Environment : {summary.environment}

--------------------------------------------------
Cluster Health
--------------------------------------------------

Nodes Ready         : {summary.ready_nodes} / {summary.total_nodes}
Namespaces          : {summary.namespaces}
Running Pods        : {summary.running_pods}
Pending Pods        : {summary.pending_pods}
Failed Pods         : {summary.failed_pods}
CrashLoopBackOff    : {summary.crashloop_pods}

Overall Status      : {"✔ Healthy" if summary.cluster_healthy else "✘ Unhealthy"}

--------------------------------------------------
Workload Status
--------------------------------------------------

Deployments Healthy : {summary.ready_deployments} / {summary.total_deployments}
StatefulSets Ready  : {summary.ready_statefulsets} / {summary.total_statefulsets}
DaemonSets Ready    : {summary.ready_daemonsets} / {summary.total_daemonsets}
"""

    # ----------------------
    # Recommendations
    # ----------------------

    recommendations = []

    if summary.cluster_healthy:
        recommendations.append("✔ Cluster is healthy.")
    else:
        recommendations.append("⚠ Cluster health requires attention.")

    if summary.pending_pods == 0:
        recommendations.append("✔ No pending pods.")
    else:
        recommendations.append(
            f"⚠ {summary.pending_pods} pod(s) are pending. Check scheduler or resources."
        )

    if summary.failed_pods == 0:
        recommendations.append("✔ No failed pods.")
    else:
        recommendations.append(
            f"⚠ {summary.failed_pods} failed pod(s) detected."
        )

    if summary.crashloop_pods == 0:
        recommendations.append("✔ No CrashLoopBackOff pods.")
    else:
        recommendations.append(
            f"⚠ {summary.crashloop_pods} pod(s) in CrashLoopBackOff."
        )

    if (
        summary.cluster_healthy
        and summary.pending_pods == 0
        and summary.failed_pods == 0
        and summary.crashloop_pods == 0
    ):
        recommendations.append("✔ No action required.")

    report += """

--------------------------------------------------
Recommendations
--------------------------------------------------

"""

    for recommendation in recommendations:
        report += recommendation + "\n"

    report += "\n=================================================="

    return report