{
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "association-execute";
  searchPaths = {
    source = [
      outputs."/melts/lib"
      outputs."/sorts/config/runtime"
      outputs."/common/utils/aws"
      outputs."/common/utils/git"
      outputs."/common/utils/sops"
      outputs."/common/utils/common"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
