{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  replace = {
    __argAirsBuild__ = inputs.product.airs-build;
    __argAirsDevelopment__ = inputs.product.airs-development;
    __argSecretsAwsDev__ = outputs."/secretsForAwsFromEnv/dev";
    __argSecretsAwsProd__ = outputs."/secretsForAwsFromEnv/airsProd";
  };
  name = "airs";
  searchPaths = {
    bin = [
      inputs.nixpkgs.awscli
      inputs.nixpkgs.findutils
      inputs.nixpkgs.gnused
      inputs.nixpkgs.gzip
      inputs.nixpkgs.nodejs
      inputs.nixpkgs.python37
      inputs.nixpkgs.utillinux
      inputs.product.makes-announce-bugsnag
      inputs.product.makes-bugsnag-source-map-uploader
    ];
  };
  entrypoint = ./entrypoint.sh;
}
