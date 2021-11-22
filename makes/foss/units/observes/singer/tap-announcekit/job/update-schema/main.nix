{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths.bin = [ outputs."/observes/bin/tap-announcekit" ];
  name = "observes-singer-tap-announcekit-job-update-schema";
  entrypoint = ./entrypoint.sh;
}
