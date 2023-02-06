{
  inputs,
  outputs,
  makeScript,
  makePythonVersion,
  ...
}:
makeScript {
  name = "integrates-execute-machine";
  replace = {
    __argScript__ = ./src/__init__.py;
  };
  searchPaths = {
    bin = [
      (makePythonVersion "3.9")
      outputs."/skims"
      outputs."/melts"
      inputs.nixpkgs.nix
    ];
    source = [
      outputs."/integrates/jobs/execute_machine/env"
      outputs."/common/utils/aws"
      outputs."/common/utils/env"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
