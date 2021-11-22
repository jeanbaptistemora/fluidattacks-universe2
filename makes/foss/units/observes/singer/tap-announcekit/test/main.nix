{ makeDerivation
, outputs
, projectPath
, ...
}:
makeDerivation {
  name = "observes-singer-tap-announcekit-test";
  env = {
    envSrc = projectPath "/observes/singer/tap_announcekit";
    envTestDir = "tests";
  };
  searchPaths = {
    source = [
      outputs."/observes/common/tester"
      outputs."/observes/singer/tap-announcekit/env/development"
    ];
  };
  builder = projectPath "/makes/foss/units/observes/common/tester/test_builder.sh";
}
