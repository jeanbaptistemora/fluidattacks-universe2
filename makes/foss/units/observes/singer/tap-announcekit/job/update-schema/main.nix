{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths.bin = [ outputs."/observes/singer/tap-announcekit/bin" ];
  name = "observes-singer-tap-announcekit-job-update-schema";
  entrypoint = ./entrypoint.sh;
}
