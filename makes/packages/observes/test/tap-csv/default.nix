{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-test-tap-csv";
  arguments = {
    envSrc = path "/observes/singer/tap_csv";
    envTestDir = "tests";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.tester
      packages.observes.env.tap-csv.development
    ];
  };
  builder = path "/makes/packages/observes/generic/tester/test_builder.sh";
}
