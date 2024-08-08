variable "subnet_ids" {
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
