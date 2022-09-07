# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "sorts";
  searchPaths = {
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
      outputs."/sorts/config/runtime"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
