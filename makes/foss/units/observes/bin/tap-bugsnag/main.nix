{ makeScript
, inputs
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run tap_bugsnag.cli main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      inputs.product.observes-env-tap-bugsnag-runtime
    ];
  };
  name = "observes-bin-tap-bugsnag";
}
