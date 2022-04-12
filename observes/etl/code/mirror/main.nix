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
      outputs."/utils/aws"
      outputs."/utils/git"
    ];
  };
  name = "observes-etl-code-mirror";
  entrypoint = ./entrypoint.sh;
}
