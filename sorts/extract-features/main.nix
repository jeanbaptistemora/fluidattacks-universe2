# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "sorts-extract-features";
  searchPaths = {
    source = [
      outputs."/melts/lib"
      outputs."/sorts/config/runtime"
      outputs."/common/utils/aws"
      outputs."/common/utils/git"
      outputs."/common/utils/sops"
      outputs."/common/utils/common"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
