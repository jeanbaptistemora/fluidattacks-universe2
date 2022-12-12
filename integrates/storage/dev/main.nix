{
  makeScript,
  outputs,
  ...
}:
makeScript {
  entrypoint = ''
    populate "true" "" --exclude "test/*"
  '';
  name = "integrates-storage-dev";
  searchPaths.source = [
    outputs."/integrates/storage/dev/lib/populate"
  ];
}
