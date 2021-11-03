{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/bin/code-etl"
      outputs."/melts"
    ];
    source = [
      (outputs."/utils/aws")
      (inputs.legacy.importUtility "git")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-job-code-etl-upload";
  entrypoint = ./entrypoint.sh;
}
