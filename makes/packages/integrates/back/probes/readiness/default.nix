{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  name = "integrates-back-probes-readiness";
  searchPaths = {
    envSources = [ packages.integrates.back.probes.lib ];
    envUtils = [ "/makes/utils/aws" ];
  };
  template = path "/makes/packages/integrates/back/probes/readiness/entrypoint.sh";
}
