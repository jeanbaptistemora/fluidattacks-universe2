{ nixpkgs
, makeEntrypoint
, path
, ...
}:
makeEntrypoint {
  name = "integrates-coverage";
  searchPaths = {
    envPaths = [
      nixpkgs.findutils
      nixpkgs.git
      nixpkgs.python37Packages.codecov
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/integrates/coverage/entrypoint.sh";
}
