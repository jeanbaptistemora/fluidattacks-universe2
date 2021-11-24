{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [ outputs."/observes/etl/zoho-crm/prepare" ];
    source = [
      outputs."/utils/aws"
      outputs."/utils/sops"
    ];
  };
  name = "observes-etl-zoho-crm-fluid-prepare";
  entrypoint = ./entrypoint.sh;
}
