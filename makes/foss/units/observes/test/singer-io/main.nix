{ inputs
, makeDerivation
, outputs
, projectPath
, ...
}:
makeDerivation {
  name = "observes-test-singer-io";
  env = {
    envSrc = projectPath "/observes/common/singer_io";
    envTestDir = "tests";
  };
  searchPaths = {
    source = [
      inputs.product.observes-generic-tester
      outputs."/observes/env/singer-io/development"
    ];
  };
  builder = projectPath "/makes/packages/observes/generic/tester/test_builder.sh";
}
