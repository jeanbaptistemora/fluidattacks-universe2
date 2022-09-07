# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "integrates-back-deploy-probes-readiness";
  searchPaths.source = [
    outputs."/common/utils/aws"
    outputs."/integrates/back/deploy/probes/lib"
  ];
  entrypoint = ./entrypoint.sh;
}
