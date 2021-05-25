{ nixpkgs
, makeDerivation
, buildPythonRequirements
, packages
, path
, ...
} @ _:
let
  pythonRequirements = buildPythonRequirements {
    name = "integrates-back-structure-pypi";
    python = nixpkgs.python37;
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
