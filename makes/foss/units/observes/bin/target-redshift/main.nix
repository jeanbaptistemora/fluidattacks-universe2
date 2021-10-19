{ makeScript
, inputs
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run target_redshift.cli main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      inputs.product.observes-env-target-redshift-runtime
    ];
  };
  name = "observes-target-redshift";
}
