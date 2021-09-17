{ makeScript
, outputs
, ...
}:
makeScript {
  entrypoint = "airs eph";
  name = "airs-eph";
  searchPaths.bin = [ outputs."/airs" ];
}
