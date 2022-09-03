{
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
      outputs."/observes/etl/gitlab"
    ];
    source = [
      outputs."/observes/common/db-creds"
    ];
  };
  name = "observes-etl-gitlab-services";
  entrypoint = ./entrypoint.sh;
}
