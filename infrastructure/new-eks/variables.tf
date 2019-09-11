variable "region" {
  default = "us-east-1"
}

variable "availability-zone-names" {
  type    = list(string)
  default = ["us-east-1a", "us-east-1b", "us-east-1d"]
}
