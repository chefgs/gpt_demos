from diagrams import Diagram, Cluster, Edge
from diagrams.azure.devops import Repos, Pipelines, Artifacts
from diagrams.azure.general import Resourcegroups
from diagrams.azure.compute import AppServices
from diagrams.azure.database import SQLDatabases, DataLake
from diagrams.azure.security import KeyVaults
# from diagrams.onprem.ci import GithubActions
from diagrams.onprem.iac import Terraform
from diagrams.custom import Custom

# Creating a diagram using Python's diagrams library to illustrate the CI/CD process for Microsoft Fabric.
with Diagram("MS-Fabric CI-CD Process with Separate Pipelines", show=False, direction="LR"):
    
    # Version Control Cluster
    with Cluster("Version Control"):
        feature_branch = Repos("Feature Branch")
        dev_branch = Repos("Dev Branch")
        main_branch = Repos("Main Branch")
        pr_review = Repos("PR Review & Approval")
    
    # PR Approval and Merge Process
    with Cluster("Pull Request Workflow"):
        feature_branch >> pr_review >> dev_branch
        dev_branch >> Edge(label="Approved & Merged") >> main_branch

    # CI Pipeline Cluster
    with Cluster("CI Pipeline"):
        ci_pipeline = Pipelines("CI Build Pipeline")
        validation = Artifacts("Validation Tests")
        dev_branch >> ci_pipeline >> validation

    # Infrastructure as Code Pipeline Cluster
    with Cluster("Infrastructure Pipeline"):
        infra_pipeline = Pipelines("Infrastructure Pipeline")
        infra_automation = Terraform("Terraform")
        infra_artifacts = Artifacts("Infra Artifacts")
        main_branch >> infra_pipeline >> infra_artifacts >> infra_automation

    # Deployment Pipeline Cluster
    with Cluster("Deployment Pipeline"):
        deploy_pipeline = Pipelines("Deployment Pipeline")
        deploy_artifacts = Artifacts("Deploy Artifacts")
        main_branch >> deploy_pipeline >> deploy_artifacts

    # Deployment Stages for Different Environments
    with Cluster("Deployment Stages"):
        
        # Dev Environment
        with Cluster("Dev Environment"):
            dev_workspace = Resourcegroups("Dev Workspace")
            dev_data_lake = DataLake("Azure Data Lake")
            dev_sql_db = SQLDatabases("Azure SQL Database")
            dev_key_vault = KeyVaults("Azure Key Vault")
            dev_app_services = AppServices("Azure App Services")
            dev_power_bi = Custom("Power BI", "./logo_resources/power_bi.png")
            
            infra_automation >> dev_workspace
            dev_workspace >> [dev_data_lake, dev_sql_db, dev_key_vault, dev_app_services, dev_power_bi]
            deploy_artifacts >> dev_app_services

        # # Stage Environment
        # with Cluster("Stage Environment"):
        #     stage_workspace = Resourcegroups("Stage Workspace")
        #     stage_data_lake = DataLake("Azure Data Lake")
        #     stage_sql_db = SQLDatabases("Azure SQL Database")
        #     stage_key_vault = KeyVaults("Azure Key Vault")
        #     stage_app_services = AppServices("Azure App Services")
        #     stage_power_bi = Custom("Power BI", "./logo_resources/power_bi.png")
            
        #     dev_workspace >> Edge(label="Promote") >> stage_workspace
        #     stage_workspace >> [stage_data_lake, stage_sql_db, stage_key_vault, stage_app_services, stage_power_bi]
        #     deploy_artifacts >> stage_app_services

        # # Production Environment
        # with Cluster("Production Environment"):
        #     prod_workspace = Resourcegroups("Production Workspace")
        #     prod_data_lake = DataLake("Azure Data Lake")
        #     prod_sql_db = SQLDatabases("Azure SQL Database")
        #     prod_key_vault = KeyVaults("Azure Key Vault")
        #     prod_app_services = AppServices("Azure App Services")
        #     prod_power_bi = Custom("Power BI", "./logo_resources/power_bi.png")
            
        #     stage_workspace >> Edge(label="Promote") >> prod_workspace
        #     prod_workspace >> [prod_data_lake, prod_sql_db, prod_key_vault, prod_app_services, prod_power_bi]
        #     deploy_artifacts >> prod_app_services