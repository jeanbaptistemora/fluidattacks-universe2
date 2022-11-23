{
  local_pkgs,
  pkgs,
  lib,
  python_version,
}: let
  pythonPkgs = pkgs."${python_version}Packages";
  aioextensions = pythonPkgs.aioextensions.overridePythonAttrs (
    old: rec {
      version = "20.11.1621472";
      src = lib.fetchPypi {
        inherit version;
        pname = old.pname;
        sha256 = "q/sqJ1kPILBICBkubJxfkymGVsATVGhQxFBbUHCozII=";
      };
    }
  );
  pathos = import ./pathos {inherit lib pythonPkgs;};
in
  pythonPkgs
  // {
    inherit aioextensions pathos;
    legacy-purity = local_pkgs.legacy-purity."${python_version}".pkg;
  }
