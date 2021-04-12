{ fetchurl
, nixpkgs
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envDb = path "/makes/applications/integrates/db";
    envDynamoZip = fetchurl {
      url = "https://s3-us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_2021-02-08.zip";
      sha256 = "01xgqk2crrnpvzr3xkd3mwiwcs6bfxqhbbyard6y8c0jgibm31pk";
    };
  };
  name = "integrates-db";
  searchPaths = {
    envPaths = [
      nixpkgs.awscli
      nixpkgs.gnused
      nixpkgs.openjdk_headless
      nixpkgs.terraform
      nixpkgs.unzip
      packages.makes.done
      packages.makes.kill-port
      packages.makes.wait
    ];
  };
  template = path "/makes/applications/integrates/db/entrypoint.sh";
}
