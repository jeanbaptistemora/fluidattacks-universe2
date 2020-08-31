resource "aws_iam_user" "backup-user" {
  name = "BackupUser"
}

resource "aws_iam_access_key" "backup-user-access-key" {
  user = aws_iam_user.backup-user.name 
}

resource "aws_iam_user" "pibe-valderrama" {
  name = "PibeValderrama"
}

resource "aws_iam_access_key" "pibe-valderrama-access-key" {
  user = aws_iam_user.pibe-valderrama.name
}


resource "aws_iam_user_policy_attachment" "backuser-attack" {
  user       = "BackupUser"
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}

