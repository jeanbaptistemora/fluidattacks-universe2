{ inputs
, makeDerivation
, outputs
, projectPath
, ...
}:
makeDerivation {
  name = "observes-test-tap-mixpanel";
  env = {
    envSrc = projectPath "/observes/singer/tap_mixpanel";
    envTestDir = "tests";
  };
  searchPaths = {
    source = [
      inputs.product.observes-generic-tester
      outputs."/observes/env/tap-mixpanel/development"
    ];
  };
  builder = projectPath "/makes/packages/observes/generic/tester/test_builder.sh";
}
