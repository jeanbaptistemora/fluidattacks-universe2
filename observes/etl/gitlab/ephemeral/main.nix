# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."${inputs.observesIndex.target.redshift.bin}"
      outputs."${inputs.observesIndex.tap.gitlab.bin}"
    ];
  };
  name = "observes-etl-gitlab-ephemeral";
  entrypoint = ./entrypoint.sh;
}
