{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-test-tap-gitlab";
  arguments = {
    envSrc = path "/observes/singer/tap_gitlab";
    envTestDir = "tests";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.tester
      packages.observes.env.tap-gitlab.development
    ];
  };
  builder = path "/makes/packages/observes/generic/tester/test_builder.sh";
}
