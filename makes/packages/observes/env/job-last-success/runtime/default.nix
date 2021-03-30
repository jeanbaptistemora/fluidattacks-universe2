{ buildPythonPackage
, makeTemplate
, nixpkgs
, packages
, path
, ...
}:
let
  pkgEnv = packages.observes.env.job-last-success;
  pythonRunReqs = pkgEnv.runtime.python;
  self = buildPythonPackage {
    name = "observes-job-last-success";
    packagePath = path "/observes/services/update_s3_last_sync_date";
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "observes-env-job-last-success-runtime";
  searchPaths = {
    envPython38Paths = [
      nixpkgs.python38Packages.psycopg2
      pythonRunReqs
      self
    ];
  };
}
