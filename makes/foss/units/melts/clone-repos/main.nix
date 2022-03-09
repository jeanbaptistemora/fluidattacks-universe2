{
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "melts-clone-repos";
  searchPaths = {
    bin = [
      outputs."/melts"
    ];
    source = [
      outputs."/utils/aws"
      outputs."/utils/git"
      outputs."/utils/sops"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
