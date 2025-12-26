variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "key_name" {
  description = "EC2 SSH key name"
  type        = string
}

variable "my_ip" {
  description = "Your public IP for SSH"
  type        = string
}