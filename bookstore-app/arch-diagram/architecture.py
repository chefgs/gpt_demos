from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB, Route53
from diagrams.aws.devtools import Codepipeline, Codebuild
from diagrams.aws.general import Client
from diagrams.onprem.network import Internet
# from diagrams.onprem.container import Docker
from diagrams.onprem.monitoring import Prometheus, Grafana
# from diagrams.programming.language import Python
from diagrams.programming.framework import React
from diagrams.custom import Custom

with Diagram("Bookstore Application Architecture", show=False, graph_attr={ 'nodesep': '0.5', 'ranksep': '1.0'}):
    client = Client("User")
    internet = Internet("Internet")
    dns = Route53("DNS")

    with Cluster("CI/CD Pipeline"):
        with Cluster("Source Code"):
            react = React("React")
            terraform = Custom("Terraform", "./tf.png")
        github_actions = Custom("GitHub Actions", "./ghactions.png")
        pipeline = Custom("GitHub Actions CICD", "./ghactions.png")

    with Cluster("AWS Cloud", graph_attr={ 'nodesep': '0.5', 'ranksep': '1.0'}):
        lb = ELB("Load Balancer")

        with Cluster("Backend Service"):
            backend = EC2("Backend (Node.js)")
            db = RDS("Database (MongoDB)")

        with Cluster("Frontend Service"):
            frontend = EC2("Frontend (React)")

        with Cluster("Monitoring"):
            prometheus = Prometheus("Prometheus")
            grafana = Grafana("Grafana")

    client >> internet >> dns >> lb
    react >> github_actions  
    terraform >> github_actions 
    github_actions >> pipeline 
    # build >> lb
    lb >> Edge(label="HTTP/HTTPS") >> frontend
    lb >> Edge(label="HTTP/HTTPS") >> backend
    backend >> Edge(label="Database Connection") >> db
    backend >> prometheus
    frontend >> prometheus
    prometheus >> grafana
