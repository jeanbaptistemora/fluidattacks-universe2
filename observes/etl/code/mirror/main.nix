{
  makeScript,
  outputs,
  inputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.nixpkgs.findutils
      outputs."/melts"
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/git"
    ];
  };
  name = "observes-etl-code-mirror";
  entrypoint = ./entrypoint.sh;
}
