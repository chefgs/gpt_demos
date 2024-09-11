from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.vcs import Github
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.container import Docker
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.network import Nginx
from diagrams.aws.compute import EC2, EKS
from diagrams.aws.network import VPC, PublicSubnet as Subnet, Nacl as SecurityGroup
from diagrams.onprem.iac import Terraform

with Diagram("CICD Pipeline", show=False, direction="LR"):
    bitbucket = Github("Bit Bucket")
    
    with Cluster("EKS"):
        with Cluster("CI Pipeline"):
            build = Jenkins("Build")
            unit_test = Jenkins("Unit Test")
            code_analysis = Prometheus("Code Analysis")
            container_build = Docker("Container Build")
            container_push = Nginx("Nexus")

    with Cluster("Infrastructure (AWS)"):
        vpc = VPC("VPC")
        with Cluster("VPC Grouping"):
            subnet = Subnet("Subnet")
            sg = SecurityGroup("Security Group")
            with Cluster("Deployment"):
                # ec2 = EC2("EC2")
                eks = EKS("EKS Cluster")
                # sg >> ec2
                sg >> eks

    terraform = Terraform("Terraform")
    bitbucket >> terraform >> Edge(label="Provision") >> vpc >> subnet >> sg
    bitbucket >> terraform >> build
    build >> unit_test >> code_analysis >> container_build >> container_push
    bitbucket >> Edge(label="Trigger") >> build >> unit_test >> code_analysis >> container_build >> container_push

    # container_push >> Edge(label="Deploy") >> ec2
    container_push >> Edge(label="Deploy") >> eks
