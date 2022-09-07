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
  name = "skims-serve-report";
  replace = {
    __argSkims__ = projectPath "/skims/skims";
  };
  searchPaths = {
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/env"
      outputs."/skims/config/runtime"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
