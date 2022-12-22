{
  outputs,
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  system = "x86_64-linux";
  pkg = (inputs.flakeAdapter {src = projectPath inputs.observesIndex.etl.dynamo.root;}).defaultNix;
  env = pkg.outputs.packages."${system}".env.bin;
  onAws = outputs."/computeOnAwsBatch/observesDynamoV2Etl";
  onAwsBig = outputs."/computeOnAwsBatch/observesDynamoV2EtlBig";
  dynamoSchema = outputs."/computeOnAwsBatch/observesDynamoSchema";
  parallelOnAws = outputs."/computeOnAwsBatch/observesDynamoParallel";
  prepareOnAws = outputs."/computeOnAwsBatch/observesDynamoPrepare";
in
  makeScript {
    searchPaths = {
      bin = [
        env
      ];
      source = [
        outputs."/observes/common/db-creds"
      ];
    };
    replace = {
      __argSendTableETL__ = "${onAws}/bin/${onAws.name}";
      __argSendBigTableETL__ = "${onAwsBig}/bin/${onAwsBig.name}";
      __argSendParallelTableETL__ = "${parallelOnAws}/bin/${parallelOnAws.name}";
      __argSendPrepare__ = "${prepareOnAws}/bin/${prepareOnAws.name}";
      __argDynamoSchema__ = "${dynamoSchema}/bin/${dynamoSchema.name}";
    };
    name = "dynamo-etl";
    entrypoint = ./entrypoint.sh;
  }
