from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.onprem.compute import Server
from diagrams.onprem.container import Docker
from diagrams.generic.database import SQL

with Diagram("Java JVM Monitoring Tech Stack", show=False):
    with Cluster("Monitoring Stack"):
        prometheus = Prometheus("Prometheus")
        grafana = Grafana("Grafana")
        alertmanager = Grafana("Alertmanager")

    with Cluster("Java Application"):
        jvm = Server("Java JVM")
        app = Docker("Java App")

    with Cluster("Database"):
        db = SQL("Database")

    jvm >> Edge(label="metrics") >> prometheus
    prometheus >> Edge(label="visualize") >> grafana
    prometheus >> Edge(label="alert") >> alertmanager
    app >> db
    app >> jvm