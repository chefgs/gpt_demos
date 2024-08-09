import os

# Define the directory structure
directories = [
    "terraform-project",
    "terraform-project/modules/vpc",
    "terraform-project/modules/subnet",
    "terraform-project/modules/security-group",
    "terraform-project/modules/ec2"
]

# Create the directories
for directory in directories:
    os.makedirs(directory, exist_ok=True)

# Define the Terraform source code for each file
terraform_files = {
    "terraform-project/main.tf": """
provider "aws" {
  region = "us-west-2"
}

module "vpc" {
  source    = "./modules/vpc"
  cidr_block = "10.0.0.0/16"
}

module "subnet" {
  source            = "./modules/subnet"
  vpc_id            = module.vpc.vpc_id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-west-2a"
}

module "security_group" {
  source = "./modules/security-group"
  vpc_id = module.vpc.vpc_id
}

module "ec2" {
  source            = "./modules/ec2"
  ami               = "ami-0abcdef1234567890"
  instance_type     = "t2.micro"
  subnet_id         = module.subnet.subnet_id
  security_group_id = module.security_group.security_group_id
}
""",
    "terraform-project/variables.tf": """
# Define any global variables if needed
""",
    "terraform-project/outputs.tf": """
output "instance_id" {
  value = module.ec2.instance_id
}
""",
    "terraform-project/modules/vpc/main.tf": """
resource "aws_vpc" "main" {
  cidr_block = var.cidr_block
}

output "vpc_id" {
  value = aws_vpc.main.id
}
""",
    "terraform-project/modules/vpc/variables.tf": """
variable "cidr_block" {
  description = "The CIDR block for the VPC"
  type        = string
}
""",
    "terraform-project/modules/vpc/outputs.tf": """
output "vpc_id" {
  value = aws_vpc.main.id
}
""",
    "terraform-project/modules/subnet/main.tf": """
resource "aws_subnet" "main" {
  vpc_id            = var.vpc_id
  cidr_block        = var.cidr_block
  availability_zone = var.availability_zone
}

output "subnet_id" {
  value = aws_subnet.main.id
}
""",
    "terraform-project/modules/subnet/variables.tf": """
variable "vpc_id" {
  description = "The ID of the VPC"
  type        = string
}

variable "cidr_block" {
  description = "The CIDR block for the subnet"
  type        = string
}

variable "availability_zone" {
  description = "The availability zone for the subnet"
  type        = string
}
""",
    "terraform-project/modules/subnet/outputs.tf": """
output "subnet_id" {
  value = aws_subnet.main.id
}
""",
    "terraform-project/modules/security-group/main.tf": """
resource "aws_security_group" "main" {
  vpc_id = var.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

output "security_group_id" {
  value = aws_security_group.main.id
}
""",
    "terraform-project/modules/security-group/variables.tf": """
variable "vpc_id" {
  description = "The ID of the VPC"
  type        = string
}
""",
    "terraform-project/modules/security-group/outputs.tf": """
output "security_group_id" {
  value = aws_security_group.main.id
}
""",
    "terraform-project/modules/ec2/main.tf": """
resource "aws_instance" "main" {
  ami           = var.ami
  instance_type = var.instance_type
  subnet_id     = var.subnet_id
  security_groups = [var.security_group_id]

  tags = {
    Name = "MyEC2Instance"
  }
}
""",
    "terraform-project/modules/ec2/variables.tf": """
variable "ami" {
  description = "The AMI ID for the EC2 instance"
  type        = string
}

variable "instance_type" {
  description = "The instance type for the EC2 instance"
  type        = string
}

variable "subnet_id" {
  description = "The ID of the subnet"
  type        = string
}

variable "security_group_id" {
  description = "The ID of the security group"
  type        = string
}
""",
    "terraform-project/modules/ec2/outputs.tf": """
output "instance_id" {
  value = aws_instance.main.id
}
"""
}

# Create the Terraform files and write the source code
for file_path, content in terraform_files.items():
    with open(file_path, "w") as file:
        file.write(content.strip())