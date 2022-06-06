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
      outputs."/common/utils/aws"
      outputs."/observes/common/db-creds"
    ];
  };
  name = "observes-etl-gitlab-product-ephemeral";
  entrypoint = ./entrypoint.sh;
}
