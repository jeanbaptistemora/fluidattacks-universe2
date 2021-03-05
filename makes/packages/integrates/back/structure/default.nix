{ nixpkgs2
, makeDerivation
, buildPythonRequirements
, packages
, path
, ...
} @ _:
let
  pythonRequirements = buildPythonRequirements {
    dependencies = [ ];
    name = "integrates-back-structure-pypi";
    python = nixpkgs2.python37;
    requirements = {
      direct = [
        "pydeps==1.9.13"
      ];
      inherited = [
        "stdlib-list==0.8.0"
      ];
    };
  };
in
makeDerivation {
  arguments = {
    envIntegratesBackModules = path "/integrates/back/packages/modules";
  };
  builder = path "/makes/packages/integrates/back/structure/builder.sh";
  name = "integrates-back-structure";
  searchPaths = {
    envPaths = [
      nixpkgs2.graphviz
      nixpkgs2.python37
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
