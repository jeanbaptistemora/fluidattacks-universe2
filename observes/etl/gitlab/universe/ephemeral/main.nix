{
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/etl/gitlab/ephemeral"
    ];
    source = [
      outputs."/observes/common/db-creds"
      outputs."/common/utils/aws"
    ];
  };
  name = "observes-etl-gitlab-universe-ephemeral";
  entrypoint = ./entrypoint.sh;
}
