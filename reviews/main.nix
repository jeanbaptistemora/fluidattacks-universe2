# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    source = [outputs."/reviews/runtime"];
  };
  name = "reviews";
  entrypoint = ./entrypoint.sh;
}
