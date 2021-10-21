{ inputs
, makeDerivation
, outputs
, projectPath
, ...
}:
makeDerivation {
  name = "observes-test-tap-csv";
  env = {
    envSrc = projectPath "/observes/singer/tap_csv";
    envTestDir = "tests";
  };
  searchPaths = {
    source = [
      inputs.product.observes-generic-tester
      outputs."/observes/env/tap-csv/development"
    ];
  };
  builder = projectPath "/makes/packages/observes/generic/tester/test_builder.sh";
}
