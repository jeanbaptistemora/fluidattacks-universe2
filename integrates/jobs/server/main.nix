# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeScript,
  outputs,
  projectPath,
  ...
}:
makeScript {
  name = "machine-serve-report";
  replace = {
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
    __argIntegratesSrc__ = projectPath "/integrates/back/src";
  };
  searchPaths = {
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/env"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
