{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    source = [
      outputs."${inputs.observesIndex.tap.announcekit.bin}"
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
    ];
  };
  name = "observes-singer-tap-announcekit-fx-test-stream";
  entrypoint = ./entrypoint.sh;
}
