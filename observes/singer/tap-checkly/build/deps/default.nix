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
    ref = "refs/tags/v1.13.0";
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
    import-linter = import ./import-linter {
      inherit lib;
      pythonPkgs = pythonPkgs2;
    };
    types-click = import ./click/stubs.nix lib;
    utils-logger = utils-logger.pkg;
  }
  // legacy
