{
  makeScript,
  outputs,
  ...
}:
makeScript {
  entrypoint = ''
    populate_storage "" --exclude "test/*"
  '';
  name = "integrates-storage-dev";
  searchPaths.source = [
    outputs."/integrates/storage/dev/lib/populate"
  ];
}
