# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "buildkite_pipeline" "main" {
  name = "universe"

  # Repo
  repository           = "https://gitlab.com/fluidattacks/universe.git" # Use HTTPS to avoid having to provide a private SSH key
  default_branch       = "trunk"
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
