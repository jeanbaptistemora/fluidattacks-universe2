{
  lib,
  pythonPkgs,
}: let
  ppft = pythonPkgs.ppft.overridePythonAttrs (
    old: rec {
      version = "1.6.6.4";
      src = lib.fetchPypi {
        inherit version;
        pname = old.pname;
        extension = "zip";
        sha256 = "RzRCzGcxhWmQvSW9a0VLuYcgAH3kUjpzxWC90AYEY9I=";
      };
    }
  );
  pox = pythonPkgs.pox.overridePythonAttrs (
    old: rec {
      version = "0.3.0";
      src = lib.fetchPypi {
        inherit version;
        pname = old.pname;
        extension = "zip";
        sha256 = "y5aDULGGRmu0kFohCEWH7Dqm/Xqg71XUFu4NUj4qvjE=";
      };
    }
  );
in
  pythonPkgs.pathos.overridePythonAttrs (
    old: rec {
      version = "0.2.8";
      src = lib.fetchPypi {
        inherit version;
        pname = old.pname;
        extension = "zip";
        sha256 = "Hw8nqQ96tmxCO6eWUpAA/ek2DRey2OUAl2Qf9AX8bxU=";
      };
      propagatedBuildInputs = [pythonPkgs.dill pythonPkgs.multiprocess pox ppft];
    }
  )
