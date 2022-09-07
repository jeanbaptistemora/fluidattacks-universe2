# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeScript,
  inputs,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
      outputs."${inputs.observesIndex.service.db_migration.env.runtime}"
    ];
  };
  name = "observes-job-migration";
  entrypoint = ./entrypoint.sh;
}
