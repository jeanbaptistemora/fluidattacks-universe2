{
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/etl/gitlab"
    ];
    source = [
      outputs."/observes/common/db-creds"
      outputs."/common/utils/aws"
    ];
  };
  name = "observes-etl-gitlab-universe";
  entrypoint = ./entrypoint.sh;
}
