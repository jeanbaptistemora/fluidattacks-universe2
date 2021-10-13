{ outputs
, inputs
, makeScript
, projectPath
, ...
}:
let
  dynamoDbEtlOnAws = outputs."/computeOnAwsBatch/observesDynamoDbIntegratesEtl";
in
makeScript {
  searchPaths = {
    bin = [
      inputs.nixpkgs.coreutils
      inputs.nixpkgs.jq
    ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  replace = {
    __argDynamoDbIntegratesEtl__ = "${dynamoDbEtlOnAws}/bin/${dynamoDbEtlOnAws.name}";
  };
  name = "observes-scheduled-on-aws-dynamodb-integrates-etl";
  entrypoint = projectPath "/makes/foss/units/observes/scheduled/on-aws/dynamodb-integrates-etl/entrypoint.sh";
}
