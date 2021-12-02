{ outputs
, inputs
, makeScript
, ...
}:
let
  onAws = outputs."/computeOnAwsBatch/observesDynamoTableEtl";
  onAws2 = outputs."/computeOnAwsBatch/observesDynamoV2TableEtl";
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
    __argSendTableETL__ = "${onAws}/bin/${onAws.name}";
    __argSendTableETL2__ = "${onAws2}/bin/${onAws2.name}";
  };
  name = "observes-etl-dynamo-integrates";
  entrypoint = ./entrypoint.sh;
}
