# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "integrates-back-authz-matrix";
  replace.__argIntegratesBackEnv__ = outputs."/integrates/back/env";
  entrypoint = ./entrypoint.sh;
}
