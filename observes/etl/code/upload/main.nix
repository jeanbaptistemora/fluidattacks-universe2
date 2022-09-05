{
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/etl/code/bin"
      outputs."/melts"
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/git"
      outputs."/common/utils/sops"
      outputs."/observes/common/db-creds"
    ];
  };
  name = "observes-etl-code-upload";
  entrypoint = ./entrypoint.sh;
}
