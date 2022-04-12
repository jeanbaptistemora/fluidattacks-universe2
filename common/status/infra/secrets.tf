variable "alertChannelUsers" {
  type = list(string)
}
variable "alertSms" {
  type = string
}
variable "bitbucketPwd" {
  sensitive = true
}
variable "bitbucketUser" {
  sensitive = true
}
variable "checklyAccountId" {
  sensitive = true
}
variable "checklyApiKey" {
  sensitive = true
}
variable "integratesApiToken" {
  sensitive = true
}

