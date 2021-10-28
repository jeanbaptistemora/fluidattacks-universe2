{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/bin/code-etl"
    ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-job-code-etl-compute-bills";
  entrypoint = ./entrypoint.sh;
}
