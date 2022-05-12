{
  inputs,
  makeScript,
  outputs,
  projectPath,
  ...
}:
makeScript {
  replace = {
    __argData__ = projectPath "/common/okta/data.yaml";
    __argScript__ = projectPath "/common/okta/close-sessions/src/__init__.py";
  };
  name = "common-okta-close-sessions";
  searchPaths = {
    bin = [inputs.nixpkgs.python39];
    source = [
      outputs."/common/okta/close-sessions/env"
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
