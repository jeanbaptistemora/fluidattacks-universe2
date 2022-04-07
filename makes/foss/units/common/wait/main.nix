{
  makeScript,
  managePorts,
  ...
}:
makeScript {
  name = "common-wait";
  searchPaths.source = [managePorts];
  entrypoint = ./entrypoint.sh;
}
