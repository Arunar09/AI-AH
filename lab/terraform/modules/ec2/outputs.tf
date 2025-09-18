output "instance_ids" {
  description = "IDs of the instances"
  value       = aws_instance.main[*].id
}

output "instance_public_ips" {
  description = "Public IPs of the instances"
  value       = aws_instance.main[*].public_ip
}

output "security_group_id" {
  description = "ID of the security group"
  value       = aws_security_group.main.id
}