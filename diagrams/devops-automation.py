from diagrams import Diagram
from diagrams.aws.compute import ECS
from diagrams.aws.management import Cloudformation
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.container import Docker
from diagrams.onprem.vcs import Git
from diagrams.k8s.controlplane import _Controlplane as Apiserver
from diagrams.k8s.compute import Pod
from diagrams.saas.chat import Slack
from diagrams.saas.communication import _Communication as Jira
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.generic.database import SQL
from diagrams.onprem.security import _Security as SonarQube

with Diagram("SDLC and DevOps Automation Architecture", show=True, direction="TB", filename="sdlc_devops_architecture"):
    # Source Code Management
    scm = Git("Source Code Repository")

    # CI/CD Tools
    ci_cd = Jenkins("CI/CD")

    # Infrastructure as Code
    iaac = Cloudformation("IaC")

    # Containerization & Orchestration
    containers = [Docker("Docker"), Apiserver("Kubernetes API"), Pod("K8s Pods")]

    # Monitoring Tools
    monitoring = [Prometheus("Prometheus"), Grafana("Grafana")]

    # Planning & Collaboration
    planning = [Jira("Jira"), Slack("Slack")]

    # Automated Testing
    testing = SonarQube("Static Code Analysis")

    # Application Deployment
    deployment = ECS("Application")

    # Database
    db = SQL("Database")

    # Linking Components
    scm >> ci_cd
    ci_cd >> iaac
    ci_cd >> testing
    iaac >> containers
    testing >> containers
    deployment >> db
    deployment >> monitoring
    ci_cd >> planning
