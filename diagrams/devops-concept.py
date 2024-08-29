from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Nginx
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.vcs import Git
from diagrams.generic.os import LinuxGeneral
from diagrams.generic.storage import Storage
from diagrams.onprem.security import Vault
from diagrams.k8s.infra import Master as Kubernetes

with Diagram("Container-Based Operating System for DevOps", show=True):

    with Cluster("Core OS"):
        kernel = LinuxGeneral("Minimal Kernel")
        container_runtime = Docker("Container Runtime")

        with Cluster("Containerized Core Services"):
            networking = Nginx("Networking Service")
            security = Vault("Security Service")
            logging = Storage("Centralized Logging")
            monitoring = Prometheus("Monitoring Service")
            observability = Grafana("Observability")

        with Cluster("CI/CD and Automation"):
            ci_cd = Jenkins("CI/CD Pipeline")
            version_control = Git("Version Control")
            orchestration = Kubernetes("Container Orchestration")

    kernel >> container_runtime

    container_runtime >> networking
    container_runtime >> security
    container_runtime >> logging
    container_runtime >> monitoring
    container_runtime >> observability

    container_runtime >> orchestration
    orchestration >> ci_cd
    orchestration >> version_control

    networking - Edge(color="darkblue") - security
    monitoring - Edge(color="darkgreen") - observability
    logging - Edge(color="brown") - monitoring

    orchestration >> Docker("Deployment Target")
