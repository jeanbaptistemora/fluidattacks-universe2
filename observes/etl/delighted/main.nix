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
      outputs."${inputs.observesIndex.tap.delighted.bin}"
      outputs."${inputs.observesIndex.tap.json.bin}"
      outputs."${inputs.observesIndex.target.redshift.bin}"
    ];
    source = [
      outputs."${inputs.observesIndex.service.job_last_success.bin}"
      outputs."/common/utils/sops"
      outputs."/observes/common/db-creds"
    ];
  };
  name = "observes-etl-delighted";
  entrypoint = ./entrypoint.sh;
}
