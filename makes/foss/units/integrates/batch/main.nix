{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  replace = {
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
  };
  name = "integrates-batch";
  searchPaths = {
    bin = [
      inputs.nixpkgs.python39
      outputs."/melts"
    ];
    source = [
      outputs."/utils/aws"
      outputs."/utils/env"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
