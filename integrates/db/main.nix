{
  makeScript,
  outputs,
  ...
}: let
  dynamodb = outputs."/integrates/db/dynamodb";
  opensearch = outputs."/integrates/db/opensearch";
  streams = outputs."/integrates/streams";
in
  makeScript {
    name = "integrates-db";
    searchPaths = {
      bin = [
        dynamodb
        opensearch
        streams
      ];
    };
    entrypoint = ./entrypoint.sh;
  }
