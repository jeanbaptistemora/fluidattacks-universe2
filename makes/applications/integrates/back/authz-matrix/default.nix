{ integratesPkgs
, makeEntrypoint
, packages
, path
, ...
} @ _:
makeEntrypoint integratesPkgs {
  arguments = {
    envIntegratesEnv = packages.integrates.back.env;
  };
  name = "integrates-back-authz-matrix";
  searchPaths = {
    envPython37Paths = [
      integratesPkgs.python37Packages.pandas
    ];
  };
  template = path "/makes/applications/integrates/back/authz-matrix/entrypoint.sh";
}
