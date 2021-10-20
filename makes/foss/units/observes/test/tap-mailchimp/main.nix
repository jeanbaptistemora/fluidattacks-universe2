{ inputs
, makeDerivation
, projectPath
, ...
}:
makeDerivation {
  name = "observes-lint-tap-mailchimp";
  env = {
    envSrc = projectPath "/observes/singer/tap_mailchimp";
    envTestDir = "tests";
  };
  searchPaths = {
    source = [
      inputs.product.observes-generic-tester
      inputs.product.observes-env-tap-mailchimp-development
    ];
  };
  builder = projectPath "/makes/packages/observes/generic/tester/test_builder.sh";
}
