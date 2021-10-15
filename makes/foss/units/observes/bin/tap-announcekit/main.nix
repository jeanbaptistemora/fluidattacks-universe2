{ makeScript
, inputs
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run tap_announcekit.cli main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      inputs.product.observes-env-tap-announcekit-runtime
    ];
  };
  name = "observes-bin-tap-announcekit";
}
