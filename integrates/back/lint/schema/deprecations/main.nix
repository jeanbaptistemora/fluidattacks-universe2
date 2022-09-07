# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeScript,
  outputs,
  ...
}:
makeScript {
  entrypoint = ./entrypoint.sh;
  name = "integrates-back-lint-schema-deprecations";
  replace.__argIntegratesBackEnv__ = outputs."/integrates/back/env";
}
