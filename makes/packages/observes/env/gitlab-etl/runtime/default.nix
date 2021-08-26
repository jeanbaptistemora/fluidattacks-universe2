{ makes
, makeTemplate
, nixpkgs
, packages
, ...
}:
with packages.observes.env;
makeTemplate {
  name = "observes-env-gitlab-etl-runtime";
  searchPaths = {
    envPaths = [
      nixpkgs.git
      packages.observes.tap-json
      packages.observes.target-redshift
    ];
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "observes-env-gitlab-etl-runtime";
        searchPaths.bin = [ nixpkgs.gcc nixpkgs.postgresql ];
        sourcesYaml = ./pypi-sources.yaml;
      })
      tap-gitlab.runtime
    ];
  };
}
