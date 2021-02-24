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
      # Order matters. In order to overwrite libraries from pypi,
      # we must attach python37Packages at the end.
      packages.asserts.pypi.runtime
      assertsPkgs.python37Packages.mysql-connector
      assertsPkgs.python37Packages.psycopg2
      assertsPkgs.python37Packages.pyodbc
      assertsPkgs.python37Packages.brotli
      assertsPkgs.python37Packages.urllib3
    ];
  };
  template = path "/makes/packages/asserts/env/template.sh";
}
