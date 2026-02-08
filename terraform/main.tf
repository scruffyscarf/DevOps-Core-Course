resource "yandex_vpc_network" "this" {
  name = "info-service-network"
}

resource "yandex_vpc_subnet" "this" {
  name           = "info-service-subnet"
  zone           = "ru-central1-a"
  network_id     = yandex_vpc_network.this.id
  v4_cidr_blocks = ["10.0.0.0/24"]
}

resource "yandex_vpc_security_group" "this" {
  name       = "info-service-security-groups"
  network_id = yandex_vpc_network.this.id

  ingress {
    protocol       = "TCP"
    port           = 22
    v4_cidr_blocks = [var.ssh_cidr]
  }

  ingress {
    protocol       = "TCP"
    port           = 80
    v4_cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    protocol       = "TCP"
    port           = 5000
    v4_cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    protocol       = "ANY"
    v4_cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "yandex_compute_instance" "vm" {
  name = var.vm_name

  resources {
    cores         = 2
    memory        = 1
    core_fraction = 20
  }

  boot_disk {
    initialize_params {
      image_id = "fd8i5gvlr8t2tcesgf2g" # Ubuntu 22.04
      size     = 10
    }
  }

  network_interface {
    subnet_id          = yandex_vpc_subnet.this.id
    nat                = true
    security_group_ids = [yandex_vpc_security_group.this.id]
  }

  metadata = {
    ssh-keys = "ubuntu:${file("~/.ssh/id_ed25519.pub")}"
  }
}

resource "github_repository" "course_repo" {
  name        = "DevOps-Core-Course"
  description = "DevOps course labs"
  visibility  = "public"

  has_issues = true
  has_wiki   = true
}
