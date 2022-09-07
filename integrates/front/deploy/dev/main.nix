# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  libGit,
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "integrates-front-deploy-dev";
  searchPaths.source = [
    libGit
    outputs."/integrates/front/deploy"
  ];
  entrypoint = ./entrypoint.sh;
}
