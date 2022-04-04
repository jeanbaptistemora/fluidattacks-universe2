{
  lib,
  system,
  local_lib,
  legacy_pkgs,
  pythonPkgs,
}: let
  python_version = "python39";
  purity_src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/purity";
    ref = "refs/tags/v1.8.0";
  };
  purity = import purity_src {
    inherit system legacy_pkgs;
    src = purity_src;
  };
  utils-logger = import local_lib.utils-logger {
    src = local_lib.utils-logger;
    inherit python_version legacy_pkgs;
  };
  postgres-client = import local_lib.postgres-client {
    src = local_lib.postgres-client;
    legacy_pkgs =
      legacy_pkgs
      // {
        python39Packages =
          legacy_pkgs.python39Packages
          // {
            utils-logger = utils-logger.pkg;
          };
      };
    inherit system local_lib;
  };
  pythonPkgs2 =
    pythonPkgs
    // {
      click = pythonPkgs.click.overridePythonAttrs (
        old: rec {
          version = "7.1.2";
          src = lib.fetchPypi {
            inherit version;
            pname = old.pname;
            sha256 = "0rUlXHxjSbwb0eWeCM0SrLvWPOZJ8liHVXg6qU37axo=";
          };
        }
      );
      types-requests = pythonPkgs.types-requests.overridePythonAttrs (
        old: rec {
          version = "2.27.16";
          src = lib.fetchPypi {
            inherit version;
            pname = old.pname;
            sha256 = "yAEMGLKRp++2CxRS2+ElMLwlaT3WV+cMYoA/zcS//ps=";
          };
        }
      );
    };
in
  pythonPkgs2
  // {
    fa-purity = purity."${python_version}".pkg;
    import-linter = import ./import-linter {
      inherit lib;
      pythonPkgs = pythonPkgs2;
    };
    pathos = import ./pathos {
      inherit lib;
      pythonPkgs = pythonPkgs2;
    };
    types-click = import ./click/stubs.nix lib;
    types-psycopg2 = import ./psycopg2/stubs.nix lib;
    utils-logger = utils-logger.pkg;
    postgres-client = postgres-client.pkg;
  }
