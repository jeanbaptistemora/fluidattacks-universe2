{ outputs
, inputs
, makeScript
, ...
}:
let
  onAws = outputs."/computeOnAwsBatch/observesDynamoTableEtl";
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
  };
  name = "observes-etl-dynamo-integrates";
  entrypoint = ./entrypoint.sh;
}
