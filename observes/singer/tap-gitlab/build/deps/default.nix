{
  lib,
  local_pkgs,
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
  aioextensions = python_pkgs.aioextensions.overridePythonAttrs (
    old: rec {
      version = "20.8.2087641";
      src = lib.fetchPypi {
        inherit version;
        pname = old.pname;
        sha256 = "rwvzxA6gT+91AXWnRUp8CjD97wTkWg2GgI+FXwLOPDA=";
      };
    }
  );
in
  python_pkgs
  // {
    inherit aioextensions;
    import-linter = import ./import-linter {
      inherit lib python_pkgs;
    };
    legacy-paginator = local_pkgs.legacy-paginator."${python_version}".pkg;
    legacy-postgres-client = local_pkgs.legacy-postgres-client."${python_version}".pkg;
    legacy-singer-io = local_pkgs.legacy-singer-io."${python_version}".pkg;
    types-click = import ./click/stubs.nix lib;
  }
