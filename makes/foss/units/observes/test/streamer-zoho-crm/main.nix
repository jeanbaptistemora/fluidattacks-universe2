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
      outputs."/observes/singer/tap-zoho-crm/env/development"
    ];
  };
  builder = projectPath "/makes/foss/units/observes/common/tester/test_builder.sh";
}
