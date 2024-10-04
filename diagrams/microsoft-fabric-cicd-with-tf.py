from diagrams import Diagram, Cluster, Edge
from diagrams.azure.devops import Repos, Pipelines
from diagrams.azure.compute import AppServices
from diagrams.azure.database import DataFactory, SynapseAnalytics, SQLDatabases
from diagrams.azure.security import KeyVaults
from diagrams.azure.storage import DataLakeStorage
from diagrams.azure.general import Resourcegroups
from diagrams.custom import Custom
from diagrams.onprem.iac import Terraform

# Create a diagram using Python's diagrams library to represent the CI/CD architecture flow for Microsoft Fabric
with Diagram("Microsoft Fabric CICD Pipeline Architecture", show=False, direction="LR"):
    # Source code management cluster
    with Cluster("Source Code Management"):
        azd_repo = Repos("Azure DevOps Repos")
        # github = GithubActions("GitHub Actions")

    # CI/CD Build pipeline cluster
    with Cluster("Build Pipeline"):
        build_pipeline = Pipelines("Azure DevOps Pipeline")

    # Resources Cluster
    with Cluster("Azure Resources"):
        resource_group = Resourcegroups("Azure Resource Group")

        # Azure Services within resource group
        with Cluster("Azure Services"):
            data_factory = DataFactory("Azure Data Factory")
            synapse = SynapseAnalytics("Azure Synapse Workspace")
            data_lake = DataLakeStorage("Azure Data Lake")
            sql_db = SQLDatabases("Azure SQL Database")
            power_bi = Custom("Power BI", "./logo_resources/power_bi.png")
            key_vault = KeyVaults("Azure Key Vault")

            # Terraform icon to depict infrastructure as code
            tf = Terraform("Terraform")

    # Connecting source code with the build pipeline
    azd_repo >> Edge(color="blue", style="solid", penwidth="2.0") >> build_pipeline
    # github >> build_pipeline

    # Build pipeline deploying to resources via Terraform
    build_pipeline >> Edge(color="blue", style="solid", penwidth="2.0") >> tf
    tf >> Edge(color="blue", style="solid", penwidth="2.0") >> resource_group
    tf >> Edge(color="blue", style="solid", penwidth="2.0") >> data_factory
    tf >> Edge(color="blue", style="solid", penwidth="2.0") >> synapse
    tf >> Edge(color="blue", style="solid", penwidth="2.0") >> data_lake
    tf >> Edge(color="blue", style="solid", penwidth="2.0") >> sql_db
    tf >> Edge(color="blue", style="solid", penwidth="2.0") >> power_bi
    tf >> Edge(color="blue", style="solid", penwidth="2.0") >> key_vault

    # Data Factory to Synapse flow
    data_factory >> Edge(color="blue", style="solid", penwidth="2.0") >> synapse
    data_factory >> Edge(color="blue", style="solid", penwidth="2.0") >> data_lake

    # Data Lake connection to Synapse
    data_lake >> Edge(color="blue", style="solid", penwidth="2.0") >> synapse

    # Synapse to SQL Database
    synapse >> Edge(color="blue", style="solid", penwidth="2.0") >> sql_db

    # Key Vault to all services for secret management
    key_vault >> Edge(color="blue", style="solid", penwidth="2.0") >> data_factory
    key_vault >> Edge(color="blue", style="solid", penwidth="2.0") >> synapse
    key_vault >> Edge(color="blue", style="solid", penwidth="2.0") >> sql_db
    key_vault >> Edge(color="blue", style="solid", penwidth="2.0") >> power_bi

    # Data flow from SQL Database to Power BI for visualization
    sql_db >> Edge(color="blue", style="solid", penwidth="2.0") >> power_bi