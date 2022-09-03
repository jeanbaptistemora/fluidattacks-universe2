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
    bin = [
      outputs."${inputs.observesIndex.service.scheduler.bin}"
    ];
    source = [
      outputs."/common/utils/sops"
    ];
  };
  name = "observes-job-scheduler";
  entrypoint = ./entrypoint.sh;
}
