{
  extras,
  legacyPkgs,
  lib,
  pythonVersion,
}: let
  pythonPkgs =
    legacyPkgs."${pythonVersion}Packages"
    // {
      fa-purity = extras.purity."${pythonVersion}".pkg;
      fa-singer-io = extras.singer-io."${pythonVersion}".pkg;
    };
  legacy = import ./legacy {
    inherit extras pythonPkgs pythonVersion;
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
          version = "2.27.20";
          src = lib.fetchPypi {
            inherit version;
            pname = old.pname;
            sha256 = "YzRFc83mxO/UTYZ8AVjZ+35r65VyHL6YgvP4V+6KU5g=";
          };
        }
      );
    };
in
  pythonPkgs2
  // {
    import-linter = import ./import-linter {
      inherit lib;
      pythonPkgs = pythonPkgs2;
    };
    types-click = import ./click/stubs.nix lib;
    types-python-dateutil = import ./dateutil/stubs.nix lib;
    utils-logger = extras.utils-logger."${pythonVersion}".pkg;
  }
  // legacy
