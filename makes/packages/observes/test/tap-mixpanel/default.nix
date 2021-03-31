{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-test-tap-mixpanel";
  arguments = {
    envSrc = path "/observes/singer/tap_mixpanel";
    envTestDir = "tests";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.tester
      packages.observes.env.tap-mixpanel.development
    ];
  };
  builder = path "/makes/packages/observes/generic/tester/test_builder.sh";
}
