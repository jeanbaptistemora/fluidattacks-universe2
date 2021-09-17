{ makeScript
, outputs
, ...
}:
makeScript {
  entrypoint = "airs dev";
  name = "airs-dev";
  searchPaths.bin = [ outputs."/airs" ];
}
