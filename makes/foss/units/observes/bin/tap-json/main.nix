{ makeScript
, inputs
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run tap_json.cli main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      inputs.product.observes-env-tap-json-runtime
    ];
  };
  name = "observes-tap-json";
}
