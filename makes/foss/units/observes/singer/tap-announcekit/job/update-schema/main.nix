{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  searchPaths.bin = [ outputs."${inputs.observesIndex.tap.announcekit.bin}" ];
  name = "observes-singer-tap-announcekit-job-update-schema";
  entrypoint = ./entrypoint.sh;
}
