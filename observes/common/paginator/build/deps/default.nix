{
  system,
  lib,
  localLib,
  legacyPkgs,
  pythonPkgs,
  pythonVersion,
}: let
  legacy-purity = import localLib.legacy-purity {
    inherit legacyPkgs pythonVersion system;
    src = localLib.legacy-purity;
  };
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
    legacy-purity = legacy-purity.pkg;
  }
