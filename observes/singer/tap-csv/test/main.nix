{
  inputs,
  makeDerivation,
  outputs,
  projectPath,
  ...
}:
makeDerivation {
  name = "observes-singer-tap-csv-test";
  env = {
    envSrc = projectPath inputs.observesIndex.tap.csv.root;
    envTestDir = "tests";
  };
  searchPaths = {
    source = [
      outputs."/observes/common/tester"
      outputs."${inputs.observesIndex.tap.csv.env.dev}"
    ];
  };
  builder = projectPath "/observes/common/tester/test_builder.sh";
}
