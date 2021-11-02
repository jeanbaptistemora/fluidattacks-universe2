{ libGit
, makeScript
, outputs
, inputs
, ...
}:
makeScript {
  name = "integrates-mock";
  searchPaths = {
    source = [
      libGit
      (inputs.legacy.importUtility "aws")
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
