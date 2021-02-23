{ assertsPkgs
, makeTemplate
, packages
, path
, ...
}:
makeTemplate assertsPkgs {
  name = "asserts-env";
  searchPaths = {
    envPaths = [
      assertsPkgs.python37
    ];
    envPythonPaths = [
      (path "/asserts")
    ];
    envPython37Paths = [
      assertsPkgs.python37Packages.mysql-connector
      assertsPkgs.python37Packages.psycopg2
      assertsPkgs.python37Packages.pyodbc
      packages.asserts.pypi.runtime
    ];
  };
  template = path "/makes/packages/asserts/env/template.sh";
}
