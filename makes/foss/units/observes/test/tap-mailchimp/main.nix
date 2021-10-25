{ makeDerivation
, outputs
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
      outputs."/observes/common/tester"
      outputs."/observes/env/tap-mailchimp/development"
    ];
  };
  builder = projectPath "/makes/foss/units/observes/common/tester/test_builder.sh";
}
