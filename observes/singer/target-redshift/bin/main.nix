{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  entrypoint = ''
    import_and_run target_redshift.cli main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      outputs."${inputs.observesIndex.target.redshift.env.runtime}"
    ];
  };
  name = "observes-target-redshift";
}
