# Master Role
resource "aws_iam_role" "k8s_master_role" {
  name = "EKSMaster"
  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
POLICY
}

resource "aws_iam_role_policy_attachment" "k8s_master_policy_1" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.k8s_master_role.name
}

resource "aws_iam_role_policy_attachment" "k8s_master_policy_2" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSServicePolicy"
  role       = aws_iam_role.k8s_master_role.name
}

# Worker Nodes Role
resource "aws_iam_role" "k8s_nodes_role" {
  name = "EKSWorkerNode"
  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
POLICY
}

resource "aws_iam_role_policy_attachment" "k8s_nodes_policy_1" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.k8s_nodes_role.name
}

resource "aws_iam_role_policy_attachment" "k8s_nodes_policy_2" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.k8s_nodes_role.name
}

resource "aws_iam_role_policy_attachment" "k8s_nodes_policy_3" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.k8s_nodes_role.name
}

# Vault Auto-Unseal Access
data "aws_iam_policy_document" "vault_unseal_access" {
  statement {
    sid = "EKSNodeKMS"
    actions = ["kms:Encrypt", "kms:Decrypt"]
    resources = [aws_kms_key.vault_encryption_key.arn]
  }

  statement {
    sid = "EKSNodeS3"
    actions = ["s3:GetObject", "s3:PutObject", "s3:ListBucket"]
    resources = [
      aws_s3_bucket.vault.arn,
      "${aws_s3_bucket.vault.arn}/*"
    ]
  }
}

resource "aws_iam_policy" "vault_unseal_policy" {
  name = "Vault_Unseal_Policy"
  path = "/"
  policy = data.aws_iam_policy_document.vault_unseal_access.json
}

resource "aws_iam_role_policy_attachment" "k8s_nodes_policy_4" {
  policy_arn = aws_iam_policy.vault_unseal_policy.arn
  role       = aws_iam_role.k8s_nodes_role.name
}

resource "aws_iam_instance_profile" "k8s_nodes_profile" {
  name = "EKSWorkerNodes"
  role = aws_iam_role.k8s_nodes_role.name
}
