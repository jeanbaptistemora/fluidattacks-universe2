{
  inputs,
  makeScript,
  outputs,
  projectPath,
  ...
}:
makeScript {
  replace = {
    __argData__ = projectPath "/common/google/data.yaml";
    __argScript__ = projectPath "/common/google/close-sessions/src/__init__.py";
  };
  name = "common-google-close-sessions";
  searchPaths = {
    bin = [inputs.nixpkgs.python39];
    source = [
      outputs."/common/google/close-sessions/env"
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
