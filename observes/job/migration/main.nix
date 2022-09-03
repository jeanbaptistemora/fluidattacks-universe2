{
  makeScript,
  inputs,
  outputs,
  ...
}:
makeScript {
  replace = {
    __argSecretsAwsProd__ = outputs."/secretsForAwsFromGitlab/prodObserves";
  };
  searchPaths = {
    source = [
      outputs."/common/utils/sops"
      outputs."${inputs.observesIndex.service.db_migration.env.runtime}"
    ];
  };
  name = "observes-job-migration";
  entrypoint = ./entrypoint.sh;
}
