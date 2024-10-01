from diagrams import Diagram, Cluster, Edge
from diagrams.azure.devops import Repos, Pipelines
from diagrams.azure.compute import AppServices
from diagrams.azure.database import DataFactory, SynapseAnalytics, SQLDatabases
from diagrams.azure.security import KeyVaults
from diagrams.azure.storage import DataLakeStorage
from diagrams.azure.general import Resourcegroups
# from diagrams.azure.analytics import PowerBIEmbedded
from diagrams.onprem.ci import GithubActions
from diagrams.generic.compute import Rack
from diagrams.custom import Custom

# from urllib.request import urlretrieve
# import ssl
# import certifi
# import urllib.request

# powerbi_url = "https://upload.wikimedia.org/wikipedia/commons/c/cf/New_Power_BI_Logo.svg"
# powerbi_icon = "Power_BI.svg"

# context = ssl.create_default_context(cafile=certifi.where())
# with urllib.request.urlopen(powerbi_url, context=context) as response, open(powerbi_icon, 'wb') as out_file:
#     out_file.write(response.read())

# powerbi_url = "https://upload.wikimedia.org/wikipedia/commons/c/cf/New_Power_BI_Logo.svg"
# powerbi_icon = "Power_BI.svg"
# urlretrieve(powerbi_url, powerbi_icon)

# Create a diagram using Python's diagrams library to represent the CI/CD architecture flow for Microsoft Fabric
with Diagram("Microsoft Fabric CICD Pipeline Architecture", show=False, direction="LR"):
    # Source code management cluster
    with Cluster("Source Code Management"):
        azd_repo = Repos("Azure DevOps Repos")
        # github = GithubActions("GitHub Actions")

    # CI/CD Build pipeline cluster
    with Cluster("Build Pipeline"):
        build_pipeline = Pipelines("Azure DevOps Pipeline")
        build_agent = Rack("Build Agent")
        build_pipeline >> build_agent

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

    # Connecting source code with the build pipeline
    azd_repo >> Edge(color="black", style="bold") >> build_pipeline
    # github >> build_pipeline

    # Build agent deploying to resources
    build_agent >> Edge(color="black", style="bold") >> resource_group
    build_agent >> Edge(color="black", style="bold") >> data_factory
    build_agent >> Edge(color="black", style="bold") >> synapse
    build_agent >> Edge(color="black", style="bold") >> data_lake
    build_agent >> Edge(color="black", style="bold") >> sql_db
    build_agent >> Edge(color="black", style="bold") >> power_bi
    build_agent >> key_vault

    # Data Factory to Synapse flow
    data_factory >> synapse
    data_factory >> data_lake

    # Data Lake connection to Synapse
    data_lake >> synapse

    # Synapse to SQL Database
    synapse >> sql_db

    # Key Vault to all services for secret management
    key_vault >> Edge(color="black", style="bold") >> data_factory
    key_vault >> Edge(color="black", style="bold") >> synapse
    key_vault >> Edge(color="black", style="bold") >> sql_db
    key_vault >> Edge(color="black", style="bold") >> power_bi

    # Data flow from SQL Database to Power BI for visualization
    sql_db >> Edge(color="black", style="bold") >> power_bi
