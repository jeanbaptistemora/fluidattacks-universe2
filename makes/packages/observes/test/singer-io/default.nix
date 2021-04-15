{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-test-singer-io";
  arguments = {
    envSrc = path "/observes/common/singer_io";
    envTestDir = "tests";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.tester
      packages.observes.env.singer-io.development
    ];
  };
  builder = path "/makes/packages/observes/generic/tester/test_builder.sh";
}
