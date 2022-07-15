{
  outputs,
  inputs,
  makeScript,
  ...
}: let
  onAws = outputs."/computeOnAwsBatch/observesDynamoV2Etl";
  onAwsBig = outputs."/computeOnAwsBatch/observesDynamoV2EtlBig";
  parallelOnAws = outputs."/computeOnAwsBatch/observesDynamoParallel";
in
  makeScript {
    searchPaths = {
      source = [
        outputs."/observes/common/db-creds"
        outputs."${inputs.observesIndex.etl.dynamo.env.runtime}"
      ];
    };
    replace = {
      __argSendTableETL__ = "${onAws}/bin/${onAws.name}";
      __argSendBigTableETL__ = "${onAwsBig}/bin/${onAwsBig.name}";
      __argSendParallelTableETL__ = "${parallelOnAws}/bin/${parallelOnAws.name}";
    };
    name = "observes-etl-dynamo-conf";
    entrypoint = ./entrypoint.sh;
  }
