variable "elb_name" {
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
