{
  legacyPkgs,
  lib,
  localLib,
  pythonVersion,
  system,
}: let
  pythonPkgs = legacyPkgs."${pythonVersion}Packages";
  purity_src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/purity";
    ref = "refs/tags/v1.15.0";
  };
  purity = import purity_src {
    inherit system;
    legacy_pkgs = legacyPkgs;
    src = purity_src;
  };
  utils-logger = import localLib.utils-logger {
    src = localLib.utils-logger;
    legacy_pkgs = legacyPkgs;
    python_version = pythonVersion;
  };
  legacy = import ./legacy {
    inherit legacyPkgs localLib pythonVersion system;
    purity = purity."${pythonVersion}".pkg;
  };
  pythonPkgs2 =
    pythonPkgs
    // {
      fa-purity = purity."${pythonVersion}".pkg;
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
    utils-logger = utils-logger.pkg;
  }
  // legacy
