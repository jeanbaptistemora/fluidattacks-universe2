{
  inputs,
  makeScript,
  outputs,
  projectPath,
  ...
}:
makeScript {
  entrypoint = ./entrypoint.sh;
  name = "integrates-streams";
  replace = {
    __argSecretsDev__ = projectPath "/integrates/secrets/development.yaml";
    __argSecretsProd__ = projectPath "/integrates/secrets/production.yaml";
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.python39
    ];
    source = [
      outputs."/common/utils/sops"
      outputs."/integrates/streams/runtime"
    ];
  };
}
