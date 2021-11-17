{ projectPath
, outputs
, makeDynamoDb
, ...
}:
makeDynamoDb
{
  name = "integrates";
  host = "127.0.0.1";
  port = "8022";
  infra = projectPath "/makes/foss/units/integrates/db/infra/";
  dataDerivation = [
    (outputs."/integrates/db/transformation")
  ];
  daemonMode = false;
}
