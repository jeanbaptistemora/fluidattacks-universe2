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
      outputs."/observes/singer/tap-gitlab/env/runtime"
    ];
  };
  name = "observes-singer-tap-gitlab-bin";
}
