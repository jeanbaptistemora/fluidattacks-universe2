{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  replace = {
    __argSecretsAwsProd__ = outputs."/secretsForAwsFromGitlab/prodObserves";
  };
  searchPaths = {
    source = [
      outputs."${inputs.observesIndex.service.batch_stability.bin}"
      outputs."/common/utils/sops"
    ];
  };
  name = "observes-job-batch-stability";
  entrypoint = ./entrypoint.sh;
}
