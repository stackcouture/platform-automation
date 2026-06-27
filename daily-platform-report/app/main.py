from kubernetes_client import get_cluster_summary
from report_generator import generate


def main():

    summary = get_cluster_summary()

    report = generate(summary)

    print(report)


if __name__ == "__main__":
    main()