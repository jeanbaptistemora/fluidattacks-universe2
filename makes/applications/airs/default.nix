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
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/source-map-uploader"
    ];
  };
  template = path "/makes/applications/airs/entrypoint.sh";
}
