{ integratesPkgs
, makeEntrypoint
, path
, ...
}:
makeEntrypoint {
  name = "integrates-coverage";
  searchPaths = {
    envPaths = [
      integratesPkgs.findutils
      integratesPkgs.git
      integratesPkgs.python37Packages.codecov
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/integrates/coverage/entrypoint.sh";
}
