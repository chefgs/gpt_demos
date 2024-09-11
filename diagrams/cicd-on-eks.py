from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.vcs import Github
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.container import Docker
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.network import Nginx
from diagrams.aws.compute import EC2, EKS
from diagrams.aws.network import VPC, PublicSubnet as Subnet, Nacl as SecurityGroup
from diagrams.onprem.iac import Terraform

with Diagram("CICD Pipeline with Terraform and EKS", show=False, direction="LR"):
    bitbucket = Github("Bit Bucket")

    with Cluster("CI Pipeline"):
        build = Jenkins("Build")
        unit_test = Jenkins("Unit Test")
        code_analysis = Prometheus("Code Analysis")
        container_build = Docker("Container Build")
        container_push = Nginx("Nexus")

        bitbucket >> Edge(label="Trigger") >> build >> unit_test >> code_analysis >> container_build >> container_push

    with Cluster("Infrastructure (AWS)"):
        vpc = VPC("VPC")
        with Cluster("VPC Grouping"):
            subnet = Subnet("Subnet")
            sg = SecurityGroup("Security Group")
            with Cluster("Deployment"):
                eks = EKS("EKS Cluster")
                sg >> eks

    terraform = Terraform("Terraform")
    bitbucket >> terraform >> Edge(label="Provision") >> vpc >> subnet >> sg
    container_push >> Edge(label="Deploy") >> eks

    # Representing Terraform code for CI/CD infrastructure creation
    with Cluster("Terraform Code"):
        tf_vpc = Terraform("VPC")
        tf_subnet = Terraform("Subnet")
        tf_sg = Terraform("Security Group")
        tf_eks = Terraform("EKS Cluster")
        tf_jenkins = Terraform("Jenkins")
        tf_nexus = Terraform("Nexus")

        terraform >> tf_vpc >> tf_subnet >> tf_sg >> tf_eks
        terraform >> tf_jenkins
        terraform >> tf_nexus