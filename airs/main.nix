{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  replace = {
    __argAirsBuild__ = outputs."/airs/build";
    __argAirsDevelopment__ = outputs."/airs/config/development";
  };
  name = "airs";
  searchPaths = {
    bin = [
      inputs.nixpkgs.awscli
      inputs.nixpkgs.findutils
      inputs.nixpkgs.gnused
      inputs.nixpkgs.gzip
      inputs.nixpkgs.nodejs-16_x
      inputs.nixpkgs.python37
      inputs.nixpkgs.utillinux
      outputs."/common/utils/bugsnag/announce"
      outputs."/common/utils/bugsnag/source-map-uploader"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
