{
  inputs,
  makePythonPypiEnvironment,
  makeScript,
  makeTemplate,
  outputs,
  projectPath,
  ...
}:
makeScript {
  replace = {
    __argGeckoDriver__ = inputs.nixpkgs.geckodriver;
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
    __argFirefox__ = inputs.nixpkgs.firefox;
  };
  name = "integrates-charts-snapshots";
  searchPaths = {
    bin = [
      inputs.nixpkgs.noto-fonts
      inputs.nixpkgs.python311
      inputs.nixpkgs.roboto
      inputs.nixpkgs.roboto-mono
      outputs."/integrates/db"
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/integrates/storage/dev/lib/populate"
      (makePythonPypiEnvironment {
        name = "integrates-charts-snapshots";
        sourcesYaml = ./pypi-sources.yaml;
      })
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
  entrypoint = projectPath "/integrates/charts/snapshots/entrypoint.sh";
}
