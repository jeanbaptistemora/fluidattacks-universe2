{ makeScript
, managePorts
, ...
}:
makeScript {
  name = "makes-wait";
  searchPaths.source = [ managePorts ];
  entrypoint = ./entrypoint.sh;
}
