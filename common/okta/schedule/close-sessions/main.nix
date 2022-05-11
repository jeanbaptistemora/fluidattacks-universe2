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
    __argScript__ = projectPath "/common/okta/schedule/close-sessions/src/__init__.py";
  };
  name = "common-okta-schedule-close-sessions";
  searchPaths = {
    bin = [inputs.nixpkgs.python39];
    source = [
      outputs."/common/okta/schedule/close-sessions/env"
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
