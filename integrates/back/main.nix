# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeScript,
  outputs,
  managePorts,
  ...
}:
makeScript {
  replace = {
    __argCertsDevelopment__ = outputs."/integrates/certs/dev";
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
  };
  name = "integrates-back";
  searchPaths.source = [
    managePorts
  ];
  entrypoint = ./entrypoint.sh;
}
