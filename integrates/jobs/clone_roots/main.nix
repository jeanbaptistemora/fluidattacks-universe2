{
  makeScript,
  makePythonVersion,
  outputs,
  inputs,
  ...
}:
makeScript {
  name = "integrates-jobs-clone-roots";
  replace = {
    __argPythonEnv__ = outputs."/integrates/jobs/clone_roots/env";
    __argScript__ = ./src/__init__.py;
  };
  searchPaths = {
    bin = [inputs.nixpkgs.nix (makePythonVersion "3.9")];
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/env"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
