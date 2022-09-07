# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeScript,
  managePorts,
  ...
}:
makeScript {
  name = "common-kill-port";
  searchPaths.source = [
    managePorts
  ];
  entrypoint = ./entrypoint.sh;
}
