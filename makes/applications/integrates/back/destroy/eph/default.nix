{ integratesPkgs
, makeEntrypoint
, path
, ...
} @ _:
makeEntrypoint integratesPkgs {
  searchPaths = {
    envPaths = [ integratesPkgs.kubectl ];
    envUtils = [ "/makes/utils/aws" ];
  };
  name = "integrates-back-destroy-eph";
  template = path "/makes/applications/integrates/back/destroy/eph/entrypoint.sh";
}
