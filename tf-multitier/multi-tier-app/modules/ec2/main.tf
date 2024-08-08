resource "aws_launch_configuration" "app_lc" {
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
}
