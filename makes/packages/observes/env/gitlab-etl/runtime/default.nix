{ makeTemplate
, nixpkgs
, packages
, ...
}:
with packages.observes.env;
makeTemplate {
  name = "observes-env-gitlab-etl-runtime";
  searchPaths = {
    envPaths = [
      gitlab-etl.runtime.python
      nixpkgs.git
      packages.observes.tap-json
      packages.observes.target-redshift
    ];
    envPython38Paths = [
      gitlab-etl.runtime.python
    ];
    envSources = [
      tap-gitlab.runtime
    ];
  };
}
