{ makeTemplate
, nixpkgs
, packages
, path
, ...
}:
with packages.observes.env;
let
  self = path "/observes/etl/dif_gitlab_etl";
in
makeTemplate {
  name = "observes-env-gitlab-etl-runtime";
  searchPaths = {
    envPaths = [
      gitlab-etl.runtime.python
      nixpkgs.git
      packages.observes.tap-json
      packages.observes.target-redshift
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      gitlab-etl.runtime.python
    ];
    envSources = [
      streamer-gitlab.runtime
    ];
  };
}
