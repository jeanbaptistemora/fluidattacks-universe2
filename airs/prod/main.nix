# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeScript,
  outputs,
  ...
}:
makeScript {
  entrypoint = "airs prod";
  name = "airs-prod";
  searchPaths.bin = [outputs."/airs"];
}
