variable "region" {
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
  default = "ami-0c55b159cbfafe1f0"
}

variable "instance_type" {
  description = "The instance type for the EC2 instances"
  default = "t2.micro"

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
  default = "multi-tier-app-db"
}

variable "allocated_storage" {
  description = "The allocated storage for the RDS instance"
  default = 20
}

variable "engine" {
  description = "The database engine for the RDS instance"
  default = "postgresql"
}

variable "engine_version" {
  description = "The engine version for the RDS instance"
  default = "11.5"
}

variable "instance_class" {
  description = "The instance class for the RDS instance"
  default = "db.t2.micro"
}

variable "db_name" {
  description = "The database name for the RDS instance"
  default = "multi-tier-app-db"
}

variable "username" {
  description = "The master username for the RDS instance"
  default = "admin"
}

variable "password" {
  description = "The master password for the RDS instance"
  default = "password"
}

variable "s3-bucket-name" {
  description = "The name of the S3 bucket"
  default = "gs-multi-tier-infra"
}

variable "dynamodb-table-name" {
  description = "The name of the DynamoDB table"
  default = "gs-terraform-lock-table"
}
