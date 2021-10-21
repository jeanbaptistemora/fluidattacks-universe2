{ makeScript
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run tap_gitlab.cli main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      outputs."/observes/env/tap-gitlab/runtime"
    ];
  };
  name = "observes-bin-tap-gitlab";
}
