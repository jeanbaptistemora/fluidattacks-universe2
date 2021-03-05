{ nixpkgs2
, makeEntrypoint
, path
, ...
}:
makeEntrypoint {
  name = "integrates-coverage";
  searchPaths = {
    envPaths = [
      nixpkgs2.findutils
      nixpkgs2.git
      nixpkgs2.python37Packages.codecov
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/integrates/coverage/entrypoint.sh";
}
