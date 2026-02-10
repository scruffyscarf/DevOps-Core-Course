variable "ssh_cidr" {
  description = "CIDR block for SSH access"
  type        = string
  default     = "192.145.30.13/32"
}

variable "vm_name" {
  description = "Name of the virtual machine"
  type        = string
  default     = "info-service"
}

variable "sa_key_file" {
  description = "Path to Yandex Cloud service account key"
  type        = string
}

variable "cloud_id" {
  type = string
}

variable "folder_id" {
  type = string
}

variable "yc_zone" {
  description = "Yandex Cloud Zone"
  type        = string
  default     = "ru-central1-a"
}

variable "ssh_public_key" {
  description = "SSH public key for VM access"
  type        = string
}
