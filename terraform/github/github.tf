terraform {
  required_providers {
    github = {
      source  = "integrations/github"
      version = "~> 6.0"
    }
  }
}

provider "github" {
  # token = "ghp_***"
  owner = "scruffyscarf"
}

resource "github_repository" "repo" {
  name        = "DevOps-Core-Course"
  description = "DevOps practice"
  visibility  = "public"
}
