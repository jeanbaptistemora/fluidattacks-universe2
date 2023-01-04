{
  makeScript,
  outputs,
  projectPath,
  ...
}:
makeScript {
  name = "forces-test";
  replace = {
    __argForcesRuntime__ = outputs."/forces/config/runtime";
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
    __argSecretsFile__ = projectPath "/integrates/secrets/development.yaml";
  };
  searchPaths = {
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
      outputs."/forces/config/development"
      outputs."/forces/config/runtime"
    ];
    bin = [
      outputs."/integrates/back"
      outputs."/integrates/db"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
