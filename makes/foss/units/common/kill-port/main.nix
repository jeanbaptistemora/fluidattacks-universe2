{
  makeScript,
  managePorts,
  ...
}:
makeScript {
  name = "common-kill-port";
  searchPaths.source = [
    managePorts
  ];
  entrypoint = ./entrypoint.sh;
}
