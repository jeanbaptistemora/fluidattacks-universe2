{ fetchUrl
, inputs
, makeScript
, projectPath
, managePorts
, ...
}:
makeScript {
  replace = {
    __argData__ = projectPath "/integrates/back/tests/data";
    __argDatabase__ = projectPath "/makes/foss/units/integrates/db/infra";
    __argNewDbDesign__ = projectPath "/integrates/arch";
    __argDynamoZip__ = fetchUrl {
      url = "https://s3-us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_2021-02-08.zip";
      sha256 = "01xgqk2crrnpvzr3xkd3mwiwcs6bfxqhbbyard6y8c0jgibm31pk";
    };
  };
  name = "integrates-db";
  searchPaths = {
    bin = [
      inputs.nixpkgs.awscli
      inputs.nixpkgs.gnused
      inputs.nixpkgs.jq
      inputs.nixpkgs.openjdk_headless
      inputs.nixpkgs.terraform
      inputs.nixpkgs.unzip
    ];
    source = [
      managePorts
    ];
  };
  entrypoint = projectPath "/makes/foss/units/integrates/db/entrypoint.sh";
}
