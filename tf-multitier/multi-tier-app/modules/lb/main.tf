resource "aws_elb" "web_elb" {
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
