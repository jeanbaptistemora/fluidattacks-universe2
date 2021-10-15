{ makeScript
, inputs
, outputs
, ...
}:
makeScript {
  entrypoint = "import_and_run tap_timedoctor main";
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      inputs.product.observes-env-tap-timedoctor-runtime
    ];
  };
  name = "observes-bin-tap-timedoctor";
}
