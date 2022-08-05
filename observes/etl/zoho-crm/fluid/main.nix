{
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [outputs."/observes/etl/zoho-crm"];
    source = [
      outputs."/common/utils/sops"
      outputs."/observes/common/db-creds"
    ];
  };
  name = "observes-etl-zoho-crm-fluid";
  entrypoint = ./entrypoint.sh;
}
