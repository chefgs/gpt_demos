import os
# import zipfile

# Directory structure
directories = [
    "multi-tier-app",
    "multi-tier-app/modules",
    "multi-tier-app/modules/vpc",
    "multi-tier-app/modules/ec2",
    "multi-tier-app/modules/rds",
    "multi-tier-app/modules/lb"
]

# Files and their contents
files = {
    "multi-tier-app/main.tf": """terraform {
  backend "s3" {
    bucket         = "my-terraform-state-bucket"
    key            = "multi-tier-app/terraform.tfstate"
    region         = "us-west-2"
    dynamodb_table = "terraform-lock-table"
  }
}

provider "aws" {
  region = var.region
}

module "vpc" {
  source = "./modules/vpc"
  vpc_cidr = var.vpc_cidr
  public_subnet_cidrs = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
}

module "ec2" {
  source = "./modules/ec2"
  ami_id = var.ami_id
  instance_type = var.instance_type
  security_groups = [module.vpc.public_subnet_ids]
  desired_capacity = var.desired_capacity
  max_size = var.max_size
  min_size = var.min_size
  subnet_ids = module.vpc.private_subnet_ids
  tags = {
    Name = "app-instance"
  }
}

module "rds" {
  source = "./modules/rds"
  subnet_ids = module.vpc.private_subnet_ids
  db_identifier = var.db_identifier
  allocated_storage = var.allocated_storage
  engine = var.engine
  engine_version = var.engine_version
  instance_class = var.instance_class
  db_name = var.db_name
  username = var.username
  password = var.password
  security_group_ids = [module.vpc.private_subnet_ids]
}

module "lb" {
  source = "./modules/lb"
  elb_name = "web-elb"
  availability_zones = ["us-west-2a", "us-west-2b"]
  security_groups = [module.vpc.public_subnet_ids]
  instance_port = 8080
  lb_port = 80
  health_check_target = "HTTP:8080/"
  health_check_interval = 30
  health_check_timeout = 5
  healthy_threshold = 2
  unhealthy_threshold = 2
}
""",
    "multi-tier-app/variables.tf": """variable "region" {
  default = "us-west-2"
}

variable "vpc_cidr" {
  default = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  default = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  default = ["10.0.3.0/24", "10.0.4.0/24"]
}

variable "ami_id" {
  description = "The AMI ID for the EC2 instances"
}

variable "instance_type" {
  description = "The instance type for the EC2 instances"
}

variable "desired_capacity" {
  description = "The desired capacity of the auto-scaling group"
  default = 1
}

variable "max_size" {
  description = "The maximum size of the auto-scaling group"
  default = 3
}

variable "min_size" {
  description = "The minimum size of the auto-scaling group"
  default = 1
}

variable "db_identifier" {
  description = "The identifier for the RDS instance"
}

variable "allocated_storage" {
  description = "The allocated storage for the RDS instance"
}

variable "engine" {
  description = "The database engine for the RDS instance"
}

variable "engine_version" {
  description = "The engine version for the RDS instance"
}

variable "instance_class" {
  description = "The instance class for the RDS instance"
}

variable "db_name" {
  description = "The database name for the RDS instance"
}

variable "username" {
  description = "The master username for the RDS instance"
}

variable "password" {
  description = "The master password for the RDS instance"
}
""",
    "multi-tier-app/modules/vpc/main.tf": """resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
  enable_dns_support = true
  enable_dns_hostnames = true
  tags = {
    Name = "main-vpc"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "main-igw"
  }
}

resource "aws_subnet" "public" {
  count = length(var.public_subnet_cidrs)
  vpc_id = aws_vpc.main.id
  cidr_block = element(var.public_subnet_cidrs, count.index)
  map_public_ip_on_launch = true
  tags = {
    Name = "public-subnet-${count.index + 1}"
  }
}

resource "aws_subnet" "private" {
  count = length(var.private_subnet_cidrs)
  vpc_id = aws_vpc.main.id
  cidr_block = element(var.private_subnet_cidrs, count.index)
  tags = {
    Name = "private-subnet-${count.index + 1}"
  }
}
""",
    "multi-tier-app/modules/vpc/variables.tf": """variable "vpc_cidr" {
  description = "The CIDR block for the VPC"
}

variable "public_subnet_cidrs" {
  description = "The CIDR blocks for the public subnets"
  type = list(string)
}

variable "private_subnet_cidrs" {
  description = "The CIDR blocks for the private subnets"
  type = list(string)
}
""",
    "multi-tier-app/modules/vpc/outputs.tf": """output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_ids" {
  value = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  value = aws_subnet.private[*].id
}
""",
    "multi-tier-app/modules/ec2/main.tf": """resource "aws_launch_configuration" "app_lc" {
  name          = "app-lc"
  image_id      = var.ami_id
  instance_type = var.instance_type
  security_groups = var.security_groups

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "app_asg" {
  desired_capacity     = var.desired_capacity
  max_size             = var.max_size
  min_size             = var.min_size
  vpc_zone_identifier  = var.subnet_ids
  launch_configuration = aws_launch_configuration.app_lc.id
  tags = var.tags
}
""",
    "multi-tier-app/modules/ec2/variables.tf": """variable "ami_id" {
  description = "The AMI ID for the EC2 instances"
}

variable "instance_type" {
  description = "The instance type for the EC2 instances"
}

variable "security_groups" {
  description = "The security groups for the EC2 instances"
  type = list(string)
}

variable "desired_capacity" {
  description = "The desired capacity of the auto-scaling group"
  default = 1
}

variable "max_size" {
  description = "The maximum size of the auto-scaling group"
  default = 3
}

variable "min_size" {
  description = "The minimum size of the auto-scaling group"
  default = 1
}

variable "subnet_ids" {
  description = "The subnet IDs for the auto-scaling group"
  type = list(string)
}

variable "tags" {
  description = "The tags for the auto-scaling group"
  type = map(string)
}
""",
    "multi-tier-app/modules/ec2/outputs.tf": """output "launch_configuration_id" {
  value = aws_launch_configuration.app_lc.id
}

output "autoscaling_group_id" {
  value = aws_autoscaling_group.app_asg.id
}
""",
    "multi-tier-app/modules/rds/main.tf": """resource "aws_db_subnet_group" "db_subnet_group" {
  name       = "db-subnet-group"
  subnet_ids = var.subnet_ids

  tags = {
    Name = "db-subnet-group"
  }
}

resource "aws_db_instance" "db" {
  identifier              = var.db_identifier
  allocated_storage       = var.allocated_storage
  engine                  = var.engine
  engine_version          = var.engine_version
  instance_class          = var.instance_class
  name                    = var.db_name
  username                = var.username
  password                = var.password
  db_subnet_group_name    = aws_db_subnet_group.db_subnet_group.name
  vpc_security_group_ids  = var.security_group_ids
  skip_final_snapshot     = true

  tags = {
    Name = var.db_identifier
  }
}
""",
    "multi-tier-app/modules/rds/variables.tf": """variable "subnet_ids" {
  description = "The subnet IDs for the RDS instance"
  type = list(string)
}

variable "db_identifier" {
  description = "The identifier for the RDS instance"
}

variable "allocated_storage" {
  description = "The allocated storage for the RDS instance"
}

variable "engine" {
  description = "The database engine for the RDS instance"
}

variable "engine_version" {
  description = "The engine version for the RDS instance"
}

variable "instance_class" {
  description = "The instance class for the RDS instance"
}

variable "db_name" {
  description = "The database name for the RDS instance"
}

variable "username" {
  description = "The master username for the RDS instance"
}

variable "password" {
  description = "The master password for the RDS instance"
}

variable "security_group_ids" {
  description = "The security group IDs for the RDS instance"
  type = list(string)
}
""",
    "multi-tier-app/modules/rds/outputs.tf": """output "db_instance_id" {
  value = aws_db_instance.db.id
}
""",
    "multi-tier-app/modules/lb/main.tf": """resource "aws_elb" "web_elb" {
  name               = var.elb_name
  availability_zones = var.availability_zones
  security_groups    = var.security_groups
  listener {
    instance_port     = var.instance_port
    instance_protocol = "HTTP"
    lb_port           = var.lb_port
    lb_protocol       = "HTTP"
  }

  health_check {
    target              = var.health_check_target
    interval            = var.health_check_interval
    timeout             = var.health_check_timeout
    healthy_threshold   = var.healthy_threshold
    unhealthy_threshold = var.unhealthy_threshold
  }

  tags = {
    Name = var.elb_name
  }
}
""",
    "multi-tier-app/modules/lb/variables.tf": """variable "elb_name" {
  description = "The name of the load balancer"
}

variable "availability_zones" {
  description = "The availability zones for the load balancer"
  type = list(string)
}

variable "security_groups" {
  description = "The security groups for the load balancer"
  type = list(string)
}

variable "instance_port" {
  description = "The instance port for the load balancer"
}

variable "lb_port" {
  description = "The load balancer port"
}

variable "health_check_target" {
  description = "The target for the health check"
}

variable "health_check_interval" {
  description = "The interval for the health check"
}

variable "health_check_timeout" {
  description = "The timeout for the health check"
}

variable "healthy_threshold" {
  description = "The healthy threshold for the health check"
}

variable "unhealthy_threshold" {
  description = "The unhealthy threshold for the health check"
}
""",
    "multi-tier-app/modules/lb/outputs.tf": """output "elb_id" {
  value = aws_elb.web_elb.id
}
"""
}

# Create directories
for directory in directories:
    os.makedirs(directory, exist_ok=True)

# Create files with content
for file_path, content in files.items():
    with open(file_path, 'w') as file:
        file.write(content)

# Create a zip file
# zip_filename = "multi-tier-app.zip"
# with zipfile.ZipFile(zip_filename, 'w') as zipf:
#     for root, _, files in os.walk("multi-tier-app"):
#         for file in files:
#             zipf.write(os.path.join(root, file))
