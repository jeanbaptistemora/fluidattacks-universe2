resource "aws_efs_file_system" "enabled" {
  creation_token = "example"
  encrypted      = false
}
