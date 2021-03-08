{ nixpkgs
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envIntegratesEnv = packages.integrates.back.env;
  };
  name = "integrates-back-authz-matrix";
  searchPaths = {
    envPython37Paths = [
      nixpkgs.python37Packages.pandas
    ];
  };
  template = path "/makes/applications/integrates/back/authz-matrix/entrypoint.sh";
}
