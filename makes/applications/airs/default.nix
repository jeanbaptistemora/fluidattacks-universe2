{ nixpkgs
, makeEntrypoint
, packages
, applications
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envAirsBuild = applications.airs.build;
    envAirsDevelopment = applications.airs.development;
  };
  name = "airs";
  searchPaths = {
    envPaths = [
      nixpkgs.findutils
      nixpkgs.gnused
      nixpkgs.gzip
      nixpkgs.nodejs
      nixpkgs.python37
      nixpkgs.utillinux
      packages.makes.announce.bugsnag
      packages.makes.bugsnag.source-map-uploader
    ];
    envUtils = [
      "/makes/utils/aws"
    ];
  };
  template = path "/makes/applications/airs/entrypoint.sh";
}
