{ outputs
, inputs
, makeScript
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
      outputs."/utils/aws"
      outputs."/utils/sops"
    ];
  };
  replace = {
    __argDynamoDbIntegratesEtl__ = "${dynamoDbEtlOnAws}/bin/${dynamoDbEtlOnAws.name}";
  };
  name = "observes-etl-dynamo-integrates";
  entrypoint = ./entrypoint.sh;
}
