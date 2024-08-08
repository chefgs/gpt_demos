terraform {
  backend "s3" {
    bucket         = "var.gs-multi-tier-infra"
    key            = "multi-tier-app/terraform.tfstate"
    region         = "us-west-2"
    dynamodb_table = "gs-terraform-lock-table"
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
