{ nixpkgs
, makeTemplate
, packages
, path
, ...
}:
makeTemplate {
  name = "asserts-env";
  searchPaths = {
    envPaths = [
      nixpkgs.git
      nixpkgs.python37
    ];
    envPythonPaths = [
      (path "/asserts")
    ];
    envPython37Paths = [
      # Order matters. In order to overwrite libraries from pypi,
      # we must attach python37Packages at the end.
      packages.asserts.pypi.runtime
      nixpkgs.python37Packages.mysql-connector
      nixpkgs.python37Packages.psycopg2
      nixpkgs.python37Packages.pyodbc
      nixpkgs.python37Packages.brotli
      nixpkgs.python37Packages.urllib3
    ];
  };
  template = path "/makes/packages/asserts/env/template.sh";
}
