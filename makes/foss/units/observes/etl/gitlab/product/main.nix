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
      outputs."/utils/aws"
      outputs."/observes/common/db-creds"
    ];
  };
  name = "observes-etl-gitlab-product";
  entrypoint = ./entrypoint.sh;
}
