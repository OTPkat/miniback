terraform {
  backend "gcs" {
    bucket = "spartan-theorem-328817-archivetf"
    prefix = "env/dev"
  }
required_providers {
    docker = {
      source  = "kreuzwerker/docker"
    }
  }
}