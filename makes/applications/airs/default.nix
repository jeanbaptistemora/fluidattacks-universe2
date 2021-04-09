{ nixpkgs
, makeEntrypoint
, packages
, applications
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envAirsContent = applications.airs.content;
  };
  name = "airs";
  searchPaths = {
    envPaths = [
      nixpkgs.findutils
      nixpkgs.gnused
      nixpkgs.gzip
      nixpkgs.python37
      packages.makes.announce.bugsnag
    ];
    envUtils = [
      "/makes/utils/aws"
    ];
  };
  template = path "/makes/applications/airs/entrypoint.sh";
}
