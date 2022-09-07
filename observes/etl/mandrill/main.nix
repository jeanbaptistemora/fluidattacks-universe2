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
      outputs."${inputs.observesIndex.target.redshift.bin}"
      outputs."${inputs.observesIndex.tap.mandrill.bin}"
    ];
    source = [
      outputs."${inputs.observesIndex.service.job_last_success.bin}"
      outputs."/common/utils/sops"
      outputs."/observes/common/db-creds"
    ];
  };
  name = "observes-etl-mandrill";
  entrypoint = ./entrypoint.sh;
}
