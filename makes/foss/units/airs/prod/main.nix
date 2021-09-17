{ makeScript
, outputs
, ...
}:
makeScript {
  entrypoint = "airs prod";
  name = "airs-prod";
  searchPaths.bin = [ outputs."/airs" ];
}
