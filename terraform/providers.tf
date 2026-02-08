terraform {
  required_version = ">= 1.5.0"

  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
      version = ">= 0.100.0"
    }

    github = {
      source  = "integrations/github"
      version = "~> 6.0"
    }
  }
}

provider "yandex" {
  service_account_key_file = "key.json"
  cloud_id = "***"
  folder_id = "***"
  zone = "ru-central1-a"
}

provider "github" {
  token = "ghp_***"
}
