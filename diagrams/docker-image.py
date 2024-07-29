from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.vcs import Github
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.container import Docker

# Create a diagram to explain the CI flow for Docker image creation
with Diagram("Docker Image Creation CI Flow", show=False):
    github = Github("GitHub Repo")
    
    with Cluster("CI Pipeline"):
        github_actions = GithubActions("GitHub Actions")
        dockerfile = Docker("Dockerfile")
        docker_image = Docker("Docker Image")
        registry = Docker("Docker Registry")

    # Flow
    github >> Edge(label="Code Check-in") >> github_actions
    github_actions >> Edge(label="Build Image") >> dockerfile
    dockerfile >> Edge(label="Create Image") >> docker_image
    docker_image >> Edge(label="Push Image") >> registry
