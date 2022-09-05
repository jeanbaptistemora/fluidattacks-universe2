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
      outputs."/common/utils/aws"
      outputs."/observes/common/db-creds"
    ];
  };
  name = "observes-etl-code-upload-migration-fa-hash";
  entrypoint = ./entrypoint.sh;
}
