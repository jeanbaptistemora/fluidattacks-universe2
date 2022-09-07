# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeScript,
  outputs,
  ...
}:
makeScript {
  entrypoint = "airs eph";
  name = "airs-eph";
  searchPaths.bin = [outputs."/airs"];
}
