{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envSrc = path "/observes/singer/tap_announcekit";
    envTestDir = "fx_tests";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.tester
      packages.observes.env.tap-announcekit.development
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "observes-fx-test-tap-announcekit";
  template = path "/makes/applications/observes/fx-test/tap-announcekit/entrypoint.sh";
}
