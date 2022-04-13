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
      outputs."/common/utils/aws"
      outputs."/common/utils/git"
      outputs."/common/utils/sops"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
