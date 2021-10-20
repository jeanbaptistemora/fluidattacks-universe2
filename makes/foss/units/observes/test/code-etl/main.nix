{ inputs
, makeDerivation
, outputs
, projectPath
, ...
}:
makeDerivation {
  builder = projectPath "/makes/packages/observes/generic/tester/test_builder.sh";
  env = {
    envSrc = projectPath "/observes/code_etl";
    envTestDir = "tests";
  };
  name = "observes-test-code-etl";
  searchPaths = {
    source = [
      inputs.product.observes-generic-tester
      outputs."/observes/env/code-etl/development"
    ];
  };
}
