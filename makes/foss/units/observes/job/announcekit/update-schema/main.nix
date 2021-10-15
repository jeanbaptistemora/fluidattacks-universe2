{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths.bin = [ outputs."/observes/bin/tap-announcekit" ];
  name = "observes-job-announcekit-update-schema";
  entrypoint = ./entrypoint.sh;
}
