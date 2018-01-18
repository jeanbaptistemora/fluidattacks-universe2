
output "sgId" {
  value = "${aws_security_group.fs_secgroup.id}"
}

output "snetId" {
  value = "${aws_subnet.fs_subnet.id}"
}
