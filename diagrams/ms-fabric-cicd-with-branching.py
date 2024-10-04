from diagrams import Diagram, Cluster, Edge
from diagrams.azure.devops import Repos, Pipelines
from diagrams.azure.general import Resourcegroups
from diagrams.azure.compute import AppServices
from diagrams.azure.database import SQLDatabases, DataLake
from diagrams.azure.security import KeyVaults
# from diagrams.azure.analytics import PowerBIEmbedded
from diagrams.azure.devops import Artifacts
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.iac import Terraform
from diagrams.generic.compute import Rack
from diagrams.custom import Custom

# Creating a diagram using Python's diagrams library to illustrate the CI/CD process for Microsoft Fabric.
with Diagram("MS-Fabric CI-CD Process with Branching Strategy and Infrastructure Automation", show=False, direction="LR"):
    
    # Version Control Cluster
    with Cluster("Version Control"):
        feature_branch = Repos("Feature Branch")
        dev_branch = Repos("Dev Branch")
        main_branch = Repos("Main Branch")
    
    # Build Pipeline Cluster
    with Cluster("Build and Validation Pipeline"):
        build_pipeline = Pipelines("CI Build Pipeline")
        validation = Rack("Validation Tests")

        feature_branch >> build_pipeline >> validation
    
    # Infrastructure as Code Cluster
    with Cluster("Infrastructure Automation"):
        infra_automation = Terraform("Infrastructure as Code (IaC)")
        deployment_artifact = Artifacts("Deployment Artifacts")
        
        build_pipeline >> deployment_artifact >> infra_automation

    # Deployment Pipelines for Different Environments
    with Cluster("Deployment Stages"):
        
        # Dev Environment
        with Cluster("Dev Environment"):
            dev_workspace = Resourcegroups("Dev Workspace")
            dev_data_lake = DataLake("Azure Data Lake")
            dev_sql_db = SQLDatabases("Azure SQL Database")
            dev_key_vault = KeyVaults("Azure Key Vault")
            dev_app_services = AppServices("Azure App Services")
            
            infra_automation >> dev_workspace
            dev_workspace >> [dev_data_lake, dev_sql_db, dev_key_vault, dev_app_services]

        # Stage Environment
        with Cluster("Stage Environment"):
            stage_workspace = Resourcegroups("Stage Workspace")
            stage_data_lake = DataLake("Azure Data Lake")
            stage_sql_db = SQLDatabases("Azure SQL Database")
            stage_key_vault = KeyVaults("Azure Key Vault")
            stage_app_services = AppServices("Azure App Services")
            
            dev_workspace >> Edge(label="Promote") >> stage_workspace
            stage_workspace >> [stage_data_lake, stage_sql_db, stage_key_vault, stage_app_services]

        # Production Environment
        with Cluster("Production Environment"):
            prod_workspace = Resourcegroups("Production Workspace")
            prod_data_lake = DataLake("Azure Data Lake")
            prod_sql_db = SQLDatabases("Azure SQL Database")
            prod_key_vault = KeyVaults("Azure Key Vault")
            prod_app_services = AppServices("Azure App Services")
            power_bi = Custom("Power BI", "./logo_resources/power_bi.png")
            
            stage_workspace >> Edge(label="Promote") >> prod_workspace
            prod_workspace >> [prod_data_lake, prod_sql_db, prod_key_vault, prod_app_services, power_bi]

    # Merge Strategy and GitHub Actions
    with Cluster("Pull Request Workflow"):
        pr_review = GithubActions("PR Review & Approval")
        pr_review >> dev_branch
        dev_branch >> Edge(label="Approved & Merged") >> main_branch

    # Linking main_branch to production release
    main_branch >> build_pipeline
