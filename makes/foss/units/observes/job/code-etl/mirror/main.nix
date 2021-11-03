{ makeScript
, outputs
, inputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.nixpkgs.findutils
      outputs."/melts"
    ];
    source = [
      (outputs."/utils/aws")
      (inputs.legacy.importUtility "git")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-job-code-etl-mirror";
  entrypoint = ./entrypoint.sh;
}
