{ libGit
, makeScript
, outputs
, ...
}:
makeScript {
  name = "integrates-mock";
  searchPaths = {
    source = [
      libGit
      outputs."/utils/aws"
    ];
    bin = [
      outputs."/integrates/batch"
      outputs."/integrates/cache"
      outputs."/integrates/db"
      outputs."/integrates/storage"
      outputs."/integrates/back"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
