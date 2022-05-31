variable "accountId" {
  sensitive = true
}
variable "alertSms" {
  type = string
}
variable "alertUsers" {
  type = list(string)
}
variable "apiKey" {
  sensitive = true
}
variable "envBitBucketPwd" {
  sensitive = true
}
variable "envBitBucketUser" {
  sensitive = true
}
variable "envIntegratesApiToken" {
  sensitive = true
}
