output "launch_configuration_id" {
  value = aws_launch_configuration.app_lc.id
}

output "autoscaling_group_id" {
  value = aws_autoscaling_group.app_asg.id
}
