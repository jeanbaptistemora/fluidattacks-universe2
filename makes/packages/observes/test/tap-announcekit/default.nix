{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-test-tap-announcekit";
  arguments = {
    envSrc = path "/observes/singer/tap_announcekit";
    envTestDir = "tests";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.tester
      packages.observes.env.tap-announcekit.development
    ];
  };
  builder = path "/makes/packages/observes/generic/tester/test_builder.sh";
}
