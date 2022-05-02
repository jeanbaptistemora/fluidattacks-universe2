{
  extras,
  lib,
  pythonPkgs,
}: let
  python_version = "python39";
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
    fa-purity = extras.purity."${python_version}".pkg;
    import-linter = import ./import-linter {
      inherit lib;
      pythonPkgs = pythonPkgs2;
    };
    pathos = import ./pathos {
      inherit lib;
      pythonPkgs = pythonPkgs2;
    };
    postgres-client = extras.postgres-client."${python_version}".pkg;
    redshift-client = extras.redshift-client."${python_version}".pkg;
    types-click = import ./click/stubs.nix lib;
    utils-logger = extras.utils-logger."${python_version}".pkg;
  }
