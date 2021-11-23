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
      outputs."/utils/aws"
      outputs."/utils/git"
      outputs."/utils/sops"
    ];
  };
  name = "observes-job-code-etl-mirror";
  entrypoint = ./entrypoint.sh;
}
