{ integratesPkgs
, makeEntrypoint
, path
, ...
} @ _:
makeEntrypoint integratesPkgs {
  arguments = { };
  name = "integrates-back-deploy-dev";
  template = path "/makes/applications/integrates/back/deploy/dev/entrypoint.sh";
}
