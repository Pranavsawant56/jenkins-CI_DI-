variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "ap-south-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "key_name" {
  description = "Exiting AWS EC2 key pair name"
  type        = string
}

variable "my_ip" {
  description = "your public ip address in CIDR notation"
  type        = string
}