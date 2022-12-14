{
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
  name = "integrates-back-test-unit";
  searchPaths = {
    bin = [
      outputs."/integrates/batch"
      outputs."/integrates/db"
    ];
    source = [
      outputs."/integrates/back/env/pypi/unit-tests"
      outputs."/integrates/storage/dev/lib/populate"
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
