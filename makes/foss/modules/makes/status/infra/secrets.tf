variable "alertChannelUsers" {
  type = list(string)
}
variable "bitbucketPwd" {
  sensitive = true
}
variable "bitbucketUser" {
  sensitive = true
}
variable "checklyApiKey" {
  sensitive = true
}
variable "integratesApiToken" {
  sensitive = true
}

