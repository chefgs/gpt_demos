variable "ami_id" {
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
