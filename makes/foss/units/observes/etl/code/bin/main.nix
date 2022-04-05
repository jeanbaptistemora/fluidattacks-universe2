{
  makeScript,
  outputs,
  ...
}:
makeScript {
  entrypoint = ''
    observes-etl-code-bin "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/etl/code/env/bin"
      outputs."/observes/common/import-and-run"
    ];
  };
  name = "observes-etl-code-bin";
}
