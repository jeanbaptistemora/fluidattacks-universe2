# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeScript,
  makeTemplate,
  outputs,
  projectPath,
  ...
}:
makeScript {
  replace = {
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
  };
  name = "integrates-charts-documents";
  searchPaths = {
    bin = [
      inputs.nixpkgs.findutils
      inputs.nixpkgs.python39
      outputs."/integrates/cache"
      outputs."/integrates/db"
      outputs."/integrates/storage"
    ];
    source = [
      outputs."/integrates/back/charts/pypi"
      outputs."/common/utils/aws"
      outputs."/common/utils/common"
      (makeTemplate {
        replace = {
          __argCriteriaVulnerabilities__ =
            projectPath "/common/criteria/src/vulnerabilities/data.yaml";
        };
        name = "charts-config-context-file";
        template = ''
          export CHARTS_CRITERIA_VULNERABILITIES='__argCriteriaVulnerabilities__'
        '';
      })
    ];
  };
  entrypoint = ./entrypoint.sh;
}
