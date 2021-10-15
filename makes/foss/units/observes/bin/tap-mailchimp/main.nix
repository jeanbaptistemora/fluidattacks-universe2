{ makeScript
, inputs
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run tap_mailchimp.cli main "$@"
  '';
  searchPaths = {
    bin = [ inputs.nixpkgs.python38 ];
    source = [
      outputs."/observes/common/import-and-run"
      inputs.product.observes-env-tap-mailchimp-runtime
    ];
  };
  name = "observes-bin-tap-mailchimp";
}
