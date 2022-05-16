{
  lib,
  pkgs,
  python_version,
}: let
  python_pkgs =
    pkgs."${python_version}Packages"
    // {
      types-requests = python_pkgs.types-requests.overridePythonAttrs (
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
  python_pkgs
  // {
    import-linter = import ./import-linter {
      inherit lib python_pkgs;
    };
    types-click = import ./click/stubs.nix lib;
  }
