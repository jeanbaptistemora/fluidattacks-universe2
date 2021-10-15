{ makeScript
, inputs
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run code_etl.cli main "$@"
  '';
  searchPaths = {
    source = [
      inputs.product.observes-env-code-etl-runtime
      outputs."/observes/common/import-and-run"
    ];
  };
  name = "observes-bin-code-etl";
}
