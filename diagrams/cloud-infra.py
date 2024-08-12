from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.network import CloudFront, APIGateway
from diagrams.aws.storage import S3
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.security import Cognito
from diagrams.aws.management import Cloudwatch
from diagrams.aws.network import Route53
from diagrams.aws.integration import SQS

with Diagram("E-commerce Website Architecture", show=False):
    
    user = Route53("User")
    
    with Cluster("Web Application Hosting"):
        s3 = S3("Static Hosting (S3)")
        cloudfront = CloudFront("CDN (CloudFront)")
        user >> cloudfront >> s3

    with Cluster("API and Backend"):
        api_gateway = APIGateway("API Gateway")
        lambda_func = Lambda("Lambda Functions")
        dynamodb = Dynamodb("NoSQL Database (DynamoDB)")
        rds = RDS("Relational Database (RDS)")
        cognito = Cognito("Authentication (Cognito)")

        api_gateway >> lambda_func
        lambda_func >> dynamodb
        lambda_func >> rds
        lambda_func >> cognito

    cloudfront >> api_gateway

    with Cluster("Monitoring and Logging"):
        cloudwatch = Cloudwatch("CloudWatch")
        lambda_func >> cloudwatch
        rds >> cloudwatch
        dynamodb >> cloudwatch

    queue = SQS("Message Queue (SQS)")
    lambda_func >> queue
