from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import Dynamodb
from diagrams.aws.storage import S3
from diagrams.aws.security import SecretsManager
from diagrams.onprem.compute import Server
from diagrams.onprem.client import Users
from diagrams.onprem.vcs import Github
from diagrams.programming.language import Python
from diagrams.onprem.network import Nginx

# Creating the architecture diagram
with Diagram("LLM Interactive App Architecture", show=True):
    user = Users("User")

    with Cluster("LLM Interactive App"):
        server = Server("App Server")
        chatbot = Python("Interactive Chatbot")
        nginx = Nginx("API Gateway")

        user >> nginx >> chatbot >> server

    with Cluster("Infrastructure as Code"):
        repo = Github("GitHub Terraform Repo")
        clone_repo = Python("Clone Repo Script")
        preprocess = Python("Preprocess Script")
        train_model = Python("Train Model Script")
        interactive_chat = Python("Interactive Chat Script")
        
        repo >> clone_repo >> preprocess >> train_model >> interactive_chat >> chatbot

    with Cluster("Cloud Environment"):
        s3 = S3("S3 Bucket (State Storage)")
        dynamodb = Dynamodb("DynamoDB (State Locking)")
        secret_mgr = SecretsManager("Secrets Manager")

        server >> Edge(label="Terraform Commands") >> s3
        server >> Edge(label="State Locking") >> dynamodb
        server >> Edge(label="Retrieve API Key") >> secret_mgr

    # Connections
    chatbot >> Edge(label="Calls API") >> secret_mgr

    interactive_chat >> server
    server >> nginx
