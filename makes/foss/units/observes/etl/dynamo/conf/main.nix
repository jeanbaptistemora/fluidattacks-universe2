{ outputs
, inputs
, makeScript
, projectPath
, ...
}:
let
  onAws = outputs."/computeOnAwsBatch/observesDynamoV2Etl";
  onAwsBig = outputs."/computeOnAwsBatch/observesDynamoTableEtlBig";
  pkg = (inputs.flakeAdapter { src = projectPath "/observes/etl/dynamo_etl_conf"; }).defaultNix;
  env = pkg.outputs.packages.x86_64-linux.env.runtime;
in
makeScript {
  searchPaths = {
    bin = [
      env
    ];
  };
  replace = {
    __argSendTableETL__ = "${onAws}/bin/${onAws.name}";
    __argSendBigTableETL__ = "${onAwsBig}/bin/${onAws.name}";
  };
  name = "observes-etl-dynamo-conf";
  entrypoint = ./entrypoint.sh;
}
