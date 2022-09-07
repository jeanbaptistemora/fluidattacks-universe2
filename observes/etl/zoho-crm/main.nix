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
      outputs."${inputs.observesIndex.tap.zoho_crm.bin}"
      outputs."${inputs.observesIndex.tap.csv.bin}"
      outputs."${inputs.observesIndex.tap.json.bin}"
      outputs."${inputs.observesIndex.target.redshift.bin}"
    ];
    source = [
      outputs."${inputs.observesIndex.service.job_last_success.bin}"
    ];
  };
  name = "observes-etl-zoho-crm";
  entrypoint = ./entrypoint.sh;
}
