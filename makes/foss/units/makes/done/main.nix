{ makeScript
, managePorts
, ...
}:
makeScript {
  name = "makes-done";
  searchPaths.source = [
    managePorts
  ];
  entrypoint = ./entrypoint.sh;
}
