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
    ];
  };
  name = "observes-etl-gitlab-default";
  entrypoint = ./entrypoint.sh;
}
