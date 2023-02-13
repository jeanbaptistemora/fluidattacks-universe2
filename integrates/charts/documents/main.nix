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
      outputs."/integrates/db"
    ];
    source = [
      outputs."/integrates/back/charts/pypi"
      outputs."/integrates/storage/dev/lib/populate"
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
