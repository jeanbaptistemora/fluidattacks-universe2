# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."${inputs.observesIndex.etl.dynamo.bin}"
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/observes/common/db-creds"
    ];
  };
  name = "observes-etl-dynamo-centralize";
  entrypoint = ./entrypoint.sh;
}
