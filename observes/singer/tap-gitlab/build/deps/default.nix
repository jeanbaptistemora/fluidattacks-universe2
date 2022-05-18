{
  lib,
  local_pkgs,
  pkgs,
  python_version,
}: let
  python_pkgs = pkgs."${python_version}Packages";
  aioextensions = python_pkgs.aioextensions.overridePythonAttrs (
    old: rec {
      version = "20.11.1621472";
      src = lib.fetchPypi {
        inherit version;
        pname = old.pname;
        sha256 = "q/sqJ1kPILBICBkubJxfkymGVsATVGhQxFBbUHCozII=";
      };
      # doCheck = false;
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
