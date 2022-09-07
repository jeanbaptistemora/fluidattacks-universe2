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
      outputs."${inputs.observesIndex.tap.dynamo.bin}"
      outputs."${inputs.observesIndex.tap.json.bin}"
      outputs."${inputs.observesIndex.target.redshift_2.bin}"
      outputs."${inputs.observesIndex.target.s3.bin}"
    ];
    source = [
      outputs."${inputs.observesIndex.service.job_last_success.bin}"
      outputs."/common/utils/aws"
      outputs."/observes/common/db-creds"
    ];
  };
  name = "observes-etl-dynamo-parallel";
  entrypoint = ./entrypoint.sh;
}
