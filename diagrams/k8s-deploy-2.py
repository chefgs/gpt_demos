from diagrams import Cluster, Diagram, Node, Edge
from diagrams.k8s.compute import Deployment, Pod
from diagrams.k8s.network import Service
from diagrams.onprem.container import Docker
from diagrams.onprem.vcs import Git
from diagrams.onprem.ci import GithubActions

with Diagram("Application Deployment", show=False, direction="TB"):  # Set direction to top-to-bottom
    dev_cluster = Cluster("Development")
    k8s_cluster = Cluster("Kubernetes Cluster")
    
    code = Git("Code Repository")
    ci_cd = GithubActions("CI/CD Pipeline")
    docker = Docker("Docker Registry")
    deployment = Deployment("Application")
    pods = Node("", nodes=[Pod("Pod") for _ in range(3)])  # Group pods into a single node
    service = Service("Service")

    # Align components vertically
    dev_cluster.add(code)
    dev_cluster.add(ci_cd)
    k8s_cluster.add(deployment)
    k8s_cluster.add(pods)
    k8s_cluster.add(service)

    # Add connections
    code - Edge(label="Push") - ci_cd
    pods >> Edge(label="Exposes") >> service
    docker - Edge(label="Pulls") - deployment
    ci_cd >> Edge(label="Builds") >> docker

