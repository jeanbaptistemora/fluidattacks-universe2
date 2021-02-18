{ integratesPkgs
, makeEntrypoint
, packages
, path
, ...
} @ _:
makeEntrypoint integratesPkgs {
  name = "integrates-back-probes-readiness";
  searchPaths = {
    envSources = [ packages.integrates.back.probes.lib ];
    envUtils = [ "/makes/utils/aws" ];
  };
  template = path "/makes/packages/integrates/back/probes/readiness/entrypoint.sh";
}
