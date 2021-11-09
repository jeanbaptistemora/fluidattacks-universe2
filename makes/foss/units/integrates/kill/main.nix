{ makeScript
, managePorts
, ...
}:
makeScript {
  name = "integrates-kill";
  searchPaths.source = [
    managePorts
  ];
  entrypoint = ./entrypoint.sh;
}
