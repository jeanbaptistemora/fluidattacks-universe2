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
  jsonschema = pythonPkgs.jsonschema.overridePythonAttrs (
    old: rec {
      version = "3.2.0";
      SETUPTOOLS_SCM_PRETEND_VERSION = version;
      src = lib.fetchPypi {
        inherit version;
        pname = old.pname;
        sha256 = "yKhbKNN3zHc35G4tnytPRO48Dh3qxr9G3e/HGH0weXo=";
      };
    }
  );
in
  pythonPkgs
  // {
    inherit jsonschema;
    legacy-purity = legacy-purity.pkg;
  }
