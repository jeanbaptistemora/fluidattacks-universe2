{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  replace = {
    __argSecretsAwsDev__ = outputs."/secretsForAwsFromGitlab/dev";
  };
  searchPaths = {
    source = [
      outputs."${inputs.observesIndex.tap.announcekit.bin}"
      outputs."/common/utils/sops"
    ];
  };
  name = "observes-singer-tap-announcekit-fx-test-stream";
  entrypoint = ./entrypoint.sh;
}
