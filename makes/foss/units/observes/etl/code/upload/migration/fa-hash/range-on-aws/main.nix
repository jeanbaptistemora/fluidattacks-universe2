{ outputs
, makeScript
, ...
}:
let
  migrate = outputs."/computeOnAwsBatch/observesCodeEtlMigration";
in
makeScript {
  searchPaths = {
    source = [
      outputs."/utils/aws"
      outputs."/utils/git"
      outputs."/utils/sops"
    ];
  };
  replace = {
    __argMigrate__ = "${migrate}/bin/${migrate.name}";
  };
  name = "observes-etl-code-upload-migration-fa-hash-range-on-aws";
  entrypoint = ./entrypoint.sh;
}
