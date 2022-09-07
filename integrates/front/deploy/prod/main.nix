# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "integrates-front-deploy-prod";
  searchPaths.source = [outputs."/integrates/front/deploy"];
  entrypoint = ./entrypoint.sh;
}
