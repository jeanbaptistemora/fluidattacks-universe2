{ inputs
, makeDerivation
, projectPath
, ...
}:
makeDerivation {
  name = "observes-test-tap-announcekit";
  env = {
    envSrc = projectPath "/observes/singer/tap_announcekit";
    envTestDir = "tests";
  };
  searchPaths = {
    source = [
      inputs.product.observes-generic-tester
      inputs.product.observes-env-tap-announcekit-development
    ];
  };
  builder = projectPath "/makes/packages/observes/generic/tester/test_builder.sh";
}
