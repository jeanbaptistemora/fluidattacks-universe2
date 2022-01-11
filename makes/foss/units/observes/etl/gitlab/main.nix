{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."${inputs.observesIndex.tap.gitlab.bin}"
      outputs."/observes/singer/tap-json/bin"
      outputs."/observes/bin/target-redshift"
    ];
  };
  name = "observes-etl-gitlab";
  entrypoint = ./entrypoint.sh;
}
