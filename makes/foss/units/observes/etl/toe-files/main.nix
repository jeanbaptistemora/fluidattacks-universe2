{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/singer/tap-toe-files/bin"
      outputs."${inputs.observesIndex.tap.json.bin}"
      outputs."/observes/bin/target-redshift"
    ];
    source = [
      outputs."/utils/aws"
      outputs."/utils/git"
      outputs."/utils/sops"
    ];
  };
  name = "observes-etl-toe-files";
  entrypoint = ./entrypoint.sh;
}
