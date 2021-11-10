{ makeScript
, outputs
, projectPath
, ...
}:
makeScript {
  name = "forces-test";
  replace = {
    __argForcesRuntime__ = outputs."/forces/config-runtime";
    __argSecretsFile__ = projectPath "/forces/secrets-dev.yaml";
  };
  searchPaths = {
    source = [
      outputs."/forces/config-development"
      outputs."/forces/config-runtime"
      outputs."/utils/sops"
      outputs."/utils/aws"
    ];
  };
  entrypoint = projectPath "/makes/foss/units/forces/test/entrypoint.sh";
}
