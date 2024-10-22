from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.compute import Server
from diagrams.onprem.vcs import Github
from diagrams.generic.os import Ubuntu

with Diagram("GitHub Actions Workflow with Self-Hosted Runner", show=False):
    github_repo = Github("GitHub Repository")

    workflow = GithubActions("Workflow")

    self_hosted_runner = Ubuntu("Self-Hosted Runner")
    
    with Cluster("Self-Hosted Runner"):
        with Cluster("Job: Build"):
            step_checkout = GithubActions("Checkout Code")
            step_build = GithubActions("Run Build")

        with Cluster("Job: Test"):
            step_test = GithubActions("Run Tests")

    github_repo >> workflow >> Edge(label="Runs-On") >> self_hosted_runner >> step_checkout >> step_build >> step_test 