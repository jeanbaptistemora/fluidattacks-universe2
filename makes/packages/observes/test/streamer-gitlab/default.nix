{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-test-streamer-gitlab";
  arguments = {
    envSrc = path "/observes/singer/streamer_gitlab";
    envTestDir = "tests";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.tester
      packages.observes.env.development.streamer-gitlab
    ];
  };
  builder = path "/makes/packages/observes/generic/tester/test_builder.sh";
}
