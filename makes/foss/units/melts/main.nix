{ makeScript
, outputs
, ...
}:
makeScript {
  name = "melts";
  searchPaths = {
    source = [ outputs."/melts/config-runtime" ];
  };
  entrypoint = ./entrypoint.sh;
}
