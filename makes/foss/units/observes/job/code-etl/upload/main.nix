{ makeScript
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
      (outputs."/utils/git")
      (outputs."/utils/sops")
    ];
  };
  name = "observes-job-code-etl-upload";
  entrypoint = ./entrypoint.sh;
}
