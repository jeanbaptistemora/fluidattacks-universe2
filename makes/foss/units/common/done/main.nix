{
  makeScript,
  managePorts,
  ...
}:
makeScript {
  name = "common-done";
  searchPaths.source = [
    managePorts
  ];
  entrypoint = ./entrypoint.sh;
}
