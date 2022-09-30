# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "buildkite_agent_token" "main" {
  description = "common-ci"
}

resource "aws_cloudformation_stack" "main" {
  name         = "common-ci"
  template_url = "https://s3.amazonaws.com/buildkite-aws-stack/v5.11.1/aws-stack.yml"
  capabilities = [
    "CAPABILITY_AUTO_EXPAND",
    "CAPABILITY_NAMED_IAM",
  ]

  parameters = {
    # Core
    BuildkiteAgentToken                = buildkite_agent_token.main.token
    BuildkiteTerminateInstanceAfterJob = false

    # Network
    VpcId                    = data.aws_vpc.main.id
    Subnets                  = data.aws_subnet.main.id
    AssociatePublicIpAddress = true

    # Workers
    InstanceType = join(
      ",",
      [
        "c5ad.large",
        "c5d.large",
      ]
    )
    EnableInstanceStorage = true
    AgentsPerInstance     = 1
    RootVolumeSize        = 10
    RootVolumeType        = "gp3"

    # Autoscaling
    MinSize                = 0
    MaxSize                = 1000
    OnDemandPercentage     = 0
    ScaleInIdlePeriod      = 1200
    ScaleOutForWaitingJobs = false
  }

  tags = {
    "Management:Area"    = "innovation"
    "Management:Product" = "common"
    "Management:Type"    = "product"
  }
}
