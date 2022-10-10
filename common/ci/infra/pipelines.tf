# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "buildkite_pipeline" "makes" {
  name = "makes"

  # Repo
  repository           = "https://github.com/fluidattacks/makes.git" # Use HTTPS to avoid having to provide a private SSH key
  default_branch       = "main"
  branch_configuration = "*"

  steps = yamlencode(
    {
      steps = [
        {
          label   = ":pipeline"
          command = "buildkite-agent pipeline upload"
        },
      ]
    }
  )
}
