{
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [outputs."/observes/etl/zoho-crm/prepare"];
    source = [
      outputs."/utils/aws"
      outputs."/utils/sops"
      outputs."/observes/common/db-creds"
    ];
  };
  name = "observes-etl-zoho-crm-fluid-prepare";
  entrypoint = ./entrypoint.sh;
}
