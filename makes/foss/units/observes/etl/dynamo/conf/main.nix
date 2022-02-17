{ outputs
, inputs
, makeScript
, ...
}:
let
  onAws = outputs."/computeOnAwsBatch/observesDynamoV2Etl";
  onAwsBig = outputs."/computeOnAwsBatch/observesDynamoV2EtlBig";
in
makeScript {
  searchPaths = {
    source = [
      outputs."${inputs.observesIndex.etl.dynamo.env.runtime}"
    ];
  };
  replace = {
    __argSendTableETL__ = "${onAws}/bin/${onAws.name}";
    __argSendBigTableETL__ = "${onAwsBig}/bin/${onAwsBig.name}";
  };
  name = "observes-etl-dynamo-conf";
  entrypoint = ./entrypoint.sh;
}
