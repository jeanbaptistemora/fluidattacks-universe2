{ inputs
, makeDerivation
, projectPath
, ...
}:
makeDerivation {
  name = "observes-test-streamer-zoho-crm";
  env = {
    envSrc = projectPath "/observes/singer/streamer_zoho_crm";
    envTestDir = "tests";
  };
  searchPaths = {
    source = [
      inputs.product.observes-generic-tester
      inputs.product.observes-env-streamer-zoho-crm-development
    ];
  };
  builder = projectPath "/makes/packages/observes/generic/tester/test_builder.sh";
}
