variable "ssh_cidr" {
  description = "CIDR block for SSH access"
  type        = string
  default     = "192.145.*.*/32"
}

variable "vm_name" {
  description = "Name of the virtual machine"
  type        = string
  default     = "info-service"
}

variable "github_token" {
  type      = string
  sensitive = true
}

variable "yc_sa_key_file" {
  description = "Path to Yandex Cloud service account key"
  type        = string
}

variable "cloud_id" {
  type = string
}

variable "folder_id" {
  type = string
}
