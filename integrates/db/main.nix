{
  inputs,
  projectPath,
  makeDynamoDb,
  makeScript,
  ...
}: let
  data = makeScript {
    replace = {
      __argDbData__ = projectPath "/integrates/back/test/data";
      __argNewDbDesign__ = projectPath "/integrates/arch/database-design.json";
    };
    name = "data-for-db";
    searchPaths = {
      bin = [
        inputs.nixpkgs.awscli
        inputs.nixpkgs.gnused
        inputs.nixpkgs.jq
      ];
    };
    entrypoint = ./data.sh;
  };
  run = makeDynamoDb {
    name = "db";
    host = "127.0.0.1";
    port = "8022";
    infra = projectPath "/integrates/db/infra";
    data = ["integrates/db/.data"];
    daemonMode = false;
  };
in
  makeScript {
    name = "dynamodb-for-integrates";
    searchPaths = {
      bin = [
        data
        run
      ];
    };
    entrypoint = ''
      data-for-db && dynamodb-for-db
    '';
  }
