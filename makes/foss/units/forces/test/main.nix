{ makeScript
, outputs
, inputs
, projectPath
, ...
}:
makeScript {
  name = "forces-test";
  replace = {
    __argForcesRuntime__ = outputs."/forces/config-runtime";
    __argSecretsFile__ = projectPath "/forces/secrets-dev.yaml";
    __argDbData__ = projectPath "/forces/test/data";
  };
  searchPaths = {
    bin = [
      outputs."/integrates/batch"
      outputs."/integrates/cache"
      outputs."/integrates/db"
      outputs."/integrates/storage"
      outputs."/integrates/back"
    ];
    source = [
      outputs."/forces/config-development"
      outputs."/forces/config-runtime"
      (inputs.legacy.importUtility "sops")
      (inputs.legacy.importUtility "aws")
    ];
  };
  entrypoint = projectPath "/makes/foss/units/forces/test/entrypoint.sh";
}
