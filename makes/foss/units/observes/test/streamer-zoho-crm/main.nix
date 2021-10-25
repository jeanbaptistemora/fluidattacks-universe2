{ makeDerivation
, outputs
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
      outputs."/observes/common/tester"
      outputs."/observes/env/streamer-zoho-crm/development"
    ];
  };
  builder = projectPath "/makes/foss/units/observes/common/tester/test_builder.sh";
}
