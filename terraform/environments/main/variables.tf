variable "project" {
  default = "spartan-theorem-328817"
}

variable "docker_image_name" {
  default = "fastgames_worker_image"
}

variable "location" {
  default = "europe-west1"
}

variable "worker_name" {
  default = "fastgames"
}

variable "db_name" {
  default = "discord-minigames"
}

variable "sql_instance_name" {
  default = "minigamesqlinstance"
}

variable "db_version" {
  default = "POSTGRES_13"
}

variable "tier" {
  default = "db-f1-micro"
}