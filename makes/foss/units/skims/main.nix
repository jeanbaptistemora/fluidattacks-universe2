{ makeScript
, outputs
, ...
}:
makeScript {
  name = "skims";
  entrypoint = ./entrypoint.sh;
  searchPaths = {
    source = [ outputs."/skims/config-runtime" ];
  };
}
