{
  makeScript,
  outputs,
  projectPath,
  inputs,
  ...
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
      outputs."/common/utils/sops"
      outputs."/common/utils/aws"
    ];
    bin = [
      inputs.nixpkgs.kubectl
    ];
  };
  entrypoint = ./entrypoint.sh;
}
