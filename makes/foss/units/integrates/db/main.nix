{ inputs
, projectPath
, makeDynamoDb
, makeScript
, ...
}:
let
  data = makeScript {
    replace = {
      __argDbData__ = projectPath "/integrates/back/tests/data";
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
    infra = projectPath "/makes/foss/units/integrates/db/infra";
    data = [ "makes/foss/units/integrates/db/.data" ];
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
