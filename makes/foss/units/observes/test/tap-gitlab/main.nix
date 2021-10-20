{ inputs
, makeDerivation
, projectPath
, ...
}:
makeDerivation {
  name = "observes-test-tap-gitlab";
  env = {
    envSrc = projectPath "/observes/singer/tap_gitlab";
    envTestDir = "tests";
  };
  searchPaths = {
    source = [
      inputs.product.observes-generic-tester
      inputs.product.observes-env-tap-gitlab-development
    ];
  };
  builder = projectPath "/makes/packages/observes/generic/tester/test_builder.sh";
}
