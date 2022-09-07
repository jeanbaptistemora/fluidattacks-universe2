# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "melts-clone-repos";
  searchPaths = {
    bin = [
      outputs."/melts"
    ];
    source = [
      outputs."/common/utils/git"
      outputs."/common/utils/sops"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
