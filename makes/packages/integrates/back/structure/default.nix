{ makes
, nixpkgs
, makeDerivation
, packages
, path
, ...
} @ _:
let
  pythonRequirements = makes.makePythonPypiEnvironment {
    name = "integrates-back-structure-pypi";
    sourcesYaml = ./pypi-sources.yaml;
  };
in
makeDerivation {
  arguments = {
    envIntegratesBackSrc = path "/integrates/back/src";
  };
  builder = path "/makes/packages/integrates/back/structure/builder.sh";
  name = "integrates-back-structure";
  searchPaths = {
    envPaths = [
      nixpkgs.findutils
      nixpkgs.gnused
      nixpkgs.graphviz
      nixpkgs.python37
      pythonRequirements
    ];
    envPython37Paths = [
      pythonRequirements
    ];
    envSources = [
      packages.integrates.back.pypi.runtime
    ];
  };
}
