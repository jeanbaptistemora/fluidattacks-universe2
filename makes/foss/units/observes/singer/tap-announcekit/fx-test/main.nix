{ inputs
, makeScript
, outputs
, projectPath
, ...
}:
makeScript {
  replace = {
    __argEnvSrc__ = projectPath inputs.observesIndex.tap.announcekit.root;
    __argEnvTestDir__ = "fx_tests";
  };
  searchPaths = {
    source = [
      outputs."/observes/common/tester"
      outputs."${inputs.observesIndex.tap.announcekit.env.dev}"
      outputs."/utils/aws"
      outputs."/utils/sops"
    ];
  };
  name = "observes-singer-tap-announcekit-fx-test";
  entrypoint = ./entrypoint.sh;
}
