from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.vcs import Git
from diagrams.onprem.container import Docker
from diagrams.onprem.compute import Server
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.programming.language import Java
from diagrams.onprem.client import Users

with Diagram("Java App CICD and Monitoring", show=False):
    developers = Users("Developers")
    with Cluster("Source Code"):
        git = Git("Git Repository")

    with Cluster("CI/CD Pipeline"):
        jenkins = Jenkins("Jenkins")
        build = jenkins >> Edge(label="Build") >> Docker("Build Image")
        package = build >> Edge(label="Package") >> Docker("Package Image")
        deploy = package >> Edge(label="Deploy") >> Server("Deploy Server")

    with Cluster("Java Application"):
        jvm = Java("Java JVM")
        app = Java("Java App")

    with Cluster("Monitoring Stack"):
        prometheus = Prometheus("Prometheus")
        grafana = Grafana("Grafana")
        alertmanager = Prometheus("Alertmanager")

    developers >> git >> jenkins
    deploy >> jvm
    jvm >> app

    jvm >> Edge(label="metrics") >> prometheus
    app >> Edge(label="metrics") >> prometheus
    prometheus >> Edge(label="visualize") >> grafana
    prometheus >> Edge(label="alert") >> alertmanager