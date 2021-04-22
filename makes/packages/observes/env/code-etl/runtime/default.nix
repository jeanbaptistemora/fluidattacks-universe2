{ makeTemplate
, nixpkgs
, packages
, path
, ...
}:
with packages.observes.env;
let
  self = path "/observes/code_etl";
in
makeTemplate {
  name = "observes-env-code-etl-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      nixpkgs.git
      code-etl.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      nixpkgs.python38Packages.psycopg2
      code-etl.runtime.python
    ];
  };
}
