{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  replace = {
    __argAirsBuild__ = outputs."/airs/build";
    __argAirsDevelopment__ = outputs."/airs/config/development";
    __argSecretsAwsDev__ = outputs."/secretsForAwsFromEnv/dev";
    __argSecretsAwsProd__ = outputs."/secretsForAwsFromEnv/prodAirs";
  };
  name = "airs";
  searchPaths = {
    bin = [
      inputs.nixpkgs.awscli
      inputs.nixpkgs.findutils
      inputs.nixpkgs.gnused
      inputs.nixpkgs.gzip
      inputs.nixpkgs.nodejs-14_x
      inputs.nixpkgs.python37
      inputs.nixpkgs.utillinux
      outputs."/makes/announce/bugsnag"
      outputs."/makes/bugsnag/source-map-uploader"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
