{ makeScript
, outputs
, ...
}:
makeScript {
  name = "forces";
  searchPaths = {
    source = [ outputs."/forces/config-runtime" ];
  };
  entrypoint = ./entrypoint.sh;
}
