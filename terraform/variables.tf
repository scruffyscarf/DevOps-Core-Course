variable "ssh_cidr" {
  description = "CIDR block for SSH access"
  type = string
  default = "192.145.*.*/32"
}

variable "vm_name" {
  description = "Name of the virtual machine"
  type = string
  default = "info-service"
}

variable "github_token" {
  type = string
  sensitive = true
}
