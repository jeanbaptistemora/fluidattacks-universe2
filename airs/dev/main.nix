# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeScript,
  outputs,
  ...
}:
makeScript {
  entrypoint = "airs dev";
  name = "airs-dev";
  searchPaths.bin = [outputs."/airs"];
}
