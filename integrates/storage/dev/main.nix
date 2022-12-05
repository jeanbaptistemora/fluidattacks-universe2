{
  makeScript,
  outputs,
  ...
}:
makeScript {
  entrypoint = "populate";
  name = "integrates-storage-dev";
  searchPaths.source = [
    outputs."/integrates/storage/dev/lib/populate"
  ];
}
