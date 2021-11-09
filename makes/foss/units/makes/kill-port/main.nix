{ makeScript
, managePorts
, ...
}:
makeScript {
  name = "makes-kill-port";
  searchPaths.source = [
    managePorts
  ];
  entrypoint = ./entrypoint.sh;
}
