{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [ outputs."/observes/etl/zoho-crm" ];
    source = [
      outputs."/utils/aws"
      outputs."/utils/sops"
    ];
  };
  name = "observes-etl-zoho-crm-fluid";
  entrypoint = ./entrypoint.sh;
}
