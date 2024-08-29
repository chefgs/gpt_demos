from diagrams import Cluster, Diagram, Edge
from diagrams.k8s.compute import Deployment, Pod
from diagrams.k8s.network import Service
from diagrams.onprem.container import Docker
from diagrams.onprem.vcs import Git
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.client import Users

with Diagram("Application Deployment", show=False, direction="LR"):
    developer = Users("Developer")

    with Cluster("Development"):
        code = Git("Code Repository")
        ci = GithubActions("CI Pipeline")
        docker_build = Docker("Docker Build") 
        docker = Docker("Docker Registry")
    
    devops_engineer = Users("DevOps Engineer")
    with Cluster("Infra Deployment"):
        kube_config = Git("Kubernetes Config")
        cd = GithubActions("CD Pipeline")

    with Cluster("Kubernetes Cluster"):
        deployment = Deployment("Application")
        pods = Pod("Pod")
        service = Service("Service")

        deployment >> pods
        pods >> service

    developer >> code
    code >> ci
    ci >> docker_build
    docker_build >> docker
    docker >> Edge(label="App Deployment") >> deployment

    devops_engineer >> kube_config
    kube_config >> cd
    cd >> deployment