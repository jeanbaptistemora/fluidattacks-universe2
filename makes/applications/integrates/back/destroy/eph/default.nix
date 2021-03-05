{ nixpkgs2
, makeEntrypoint
, path
, ...
}:
makeEntrypoint {
  searchPaths = {
    envPaths = [ nixpkgs2.kubectl ];
    envUtils = [ "/makes/utils/aws" ];
  };
  name = "integrates-back-destroy-eph";
  template = path "/makes/applications/integrates/back/destroy/eph/entrypoint.sh";
}
