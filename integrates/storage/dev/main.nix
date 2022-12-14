{
  makeScript,
  outputs,
  ...
}:
makeScript {
  entrypoint = ./entrypoint.sh;
  name = "integrates-storage-dev";
  searchPaths.source = [outputs."/integrates/storage/dev/lib/populate"];
}
