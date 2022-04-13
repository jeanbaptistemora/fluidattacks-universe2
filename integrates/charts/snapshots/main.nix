{
  inputs,
  makePythonPypiEnvironment,
  makeScript,
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
      inputs.nixpkgs.python39
      outputs."/integrates/cache"
      outputs."/integrates/db"
      outputs."/integrates/storage"
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "integrates-charts-snapshots";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/common/utils/aws"
    ];
  };
  entrypoint = projectPath "/integrates/charts/snapshots/entrypoint.sh";
}
