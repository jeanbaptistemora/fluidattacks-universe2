{
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/etl/code/bin"
    ];
    source = [
      outputs."/utils/aws"
      outputs."/utils/sops"
      outputs."/observes/common/db-creds"
    ];
  };
  name = "observes-etl-code-compute-bills";
  entrypoint = ./entrypoint.sh;
}
