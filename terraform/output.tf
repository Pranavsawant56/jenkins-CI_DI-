output "ec2_public_ip" {
  description = "Public IP address of EC2 instance"
  value       = aws_instance.jenkins_server.public_ip
}


output "ec2_public_dns" {
  description = "Public DNS name of the EC2 instance"
  value       = aws_instance.jenkins_server.public_dns
}