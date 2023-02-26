{
  inputs,
  makeScript,
  outputs,
  projectPath,
  ...
}:
makeScript {
  replace = {
    __argSecretsDev__ = projectPath "/integrates/secrets/development.yaml";
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.kubectl
      inputs.nixpkgs.python39
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
      outputs."/integrates/web/testrigor/runtime"
    ];
  };
  name = "integrates-web-testrigor";
  entrypoint = ./entrypoint.sh;
}
