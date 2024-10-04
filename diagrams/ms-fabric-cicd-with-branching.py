from diagrams import Diagram, Cluster, Edge
from diagrams.azure.devops import Repos, Pipelines, Artifacts
from diagrams.azure.general import Resourcegroups
from diagrams.azure.compute import AppServices
from diagrams.azure.database import SQLDatabases, DataLake
from diagrams.azure.security import KeyVaults
from diagrams.azure.analytics import SynapseAnalytics, DataFactories
from diagrams.onprem.iac import Terraform
from diagrams.custom import Custom
from diagrams.onprem.client import Users
from diagrams.azure.devops import Pipelines

# Creating a diagram using Python's diagrams library to illustrate the CI/CD process for Microsoft Fabric.
with Diagram("MS-Fabric CI-CD Process with Separate Pipelines", show=False, direction="LR"):
    # User Personas
    developers = Users("Developers")
    devops_engineers = Users("DevOps Engineers")

    # Version Control Cluster
    with Cluster("Azure Repos"):
        feature_branch = Repos("Feature Branch")
        dev_branch = Repos("Dev Branch")
        stage_branch = Repos("Stage Branch")
        main_branch = Repos("Main Branch")
        devops_engineers >> Pipelines("DevOps Pipeline Repo")
    
    # PR Approval and Merge Process
    # with Cluster("PR Review Process"):
        pr_review = Repos("PR Review & Approval")
        developers >> feature_branch >> pr_review >> dev_branch
        dev_branch >> Edge(label="Approved & Merged") >> stage_branch
        stage_branch >> Edge(label="Approved & Merged") >> main_branch

    # CI Pipeline Cluster
    with Cluster("CI Pipeline"):
        ci_pipeline = Pipelines("CI Build Pipeline")
        validation = Artifacts("Validation Tests")
        dev_branch >> ci_pipeline >> validation

    # Infrastructure as Code Pipeline Cluster
    with Cluster("Infrastructure Pipeline"):
        infra_repo = Repos("Terraform IaC Code")
        infra_pipeline = Pipelines("Infrastructure Pipeline")
        infra_automation = Terraform("Terraform")
        devops_engineers >> infra_repo >> infra_pipeline >> infra_automation

    # Deployment Pipeline Cluster
    with Cluster("Deployment Pipeline"):
        deploy_pipeline = Pipelines("Deployment Pipeline")
        deploy_artifacts = Artifacts("Deploy Artifacts")
        validation >> Edge(label="Trigger") >> deploy_pipeline >> deploy_artifacts

    # Deployment Stages for Different Environments
    with Cluster("Deployment Stages"):
        
        # Dev Environment
        with Cluster("Dev Environment"):
            dev_workspace = Resourcegroups("Dev Workspace")
            dev_data_lake = DataLake("Azure Data Lake")
            dev_data_factory = DataFactories("Azure Data Factory")
            dev_synapse = SynapseAnalytics("Azure Synapse")
            dev_sql_db = SQLDatabases("Azure SQL Database")
            dev_key_vault = KeyVaults("Azure Key Vault")
            # dev_app_services = AppServices("Azure App Services")
            # dev_api_services = AppServices("Azure API Services")
            dev_power_bi = Custom("Power BI", "./logo_resources/power_bi.png")
            
            infra_automation >> dev_workspace
            dev_workspace >> [dev_data_lake, dev_data_factory, dev_synapse, dev_sql_db, dev_power_bi]
            # dev_sql_db >> dev_app_services >> dev_api_services >> dev_power_bi
            # dev_workspace >> dev_key_vault
            deploy_artifacts >> dev_workspace

                # Data Factory to Synapse flow
    dev_data_factory >> dev_synapse
    dev_data_factory >> dev_data_lake

    # Data Lake connection to Synapse
    dev_data_lake >> dev_synapse

    # Synapse to SQL Database
    dev_synapse >> dev_sql_db >> dev_power_bi


        # Stage Environment
        # with Cluster("Stage Environment"):
        #     stage_workspace = Resourcegroups("Stage Workspace")
        #     stage_data_lake = DataLake("Azure Data Lake")
        #     stage_data_factory = DataFactories("Azure Data Factory")
        #     stage_synapse = SynapseAnalytics("Azure Synapse")
        #     stage_sql_db = SQLDatabases("Azure SQL Database")
        #     stage_key_vault = KeyVaults("Azure Key Vault")
        #     stage_app_services = AppServices("Azure App Services")
        #     stage_api_services = AppServices("Azure API Services")
        #     stage_power_bi = Custom("Power BI", "./logo_resources/power_bi.png")
            
        #     infra_automation >> stage_workspace
        #     dev_workspace >> Edge(label="Promote") >> stage_workspace
        #     stage_workspace >> stage_data_lake >> stage_data_factory >> stage_synapse >> stage_sql_db
        #     stage_sql_db >> stage_app_services >> stage_api_services >> stage_power_bi
        #     stage_workspace >> stage_key_vault
        #     deploy_artifacts >> stage_workspace

        # # Production Environment
        # with Cluster("Production Environment"):
        #     prod_workspace = Resourcegroups("Production Workspace")
        #     prod_data_lake = DataLake("Azure Data Lake")
        #     prod_data_factory = DataFactories("Azure Data Factory")
        #     prod_synapse = SynapseAnalytics("Azure Synapse")
        #     prod_sql_db = SQLDatabases("Azure SQL Database")
        #     prod_key_vault = KeyVaults("Azure Key Vault")
        #     prod_app_services = AppServices("Azure App Services")
        #     prod_api_services = AppServices("Azure API Services")
        #     prod_power_bi = Custom("Power BI", "./logo_resources/power_bi.png")
            
        #     infra_automation >> prod_workspace
        #     stage_workspace >> Edge(label="Promote") >> prod_workspace
        #     prod_workspace >> prod_data_lake >> prod_data_factory >> prod_synapse >> prod_sql_db
        #     prod_sql_db >> prod_app_services >> prod_api_services >> prod_power_bi
        #     prod_workspace >> prod_key_vault
        #     deploy_artifacts >> prod_workspace