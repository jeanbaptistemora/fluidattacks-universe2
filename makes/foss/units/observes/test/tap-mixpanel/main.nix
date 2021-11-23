{ makeDerivation
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
      outputs."/observes/common/tester"
      outputs."/observes/singer/tap-mixpanel/env/development"
    ];
  };
  builder = projectPath "/makes/foss/units/observes/common/tester/test_builder.sh";
}
