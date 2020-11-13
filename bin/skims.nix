let
  pkgs = import ../build/pkgs/skims.nix;

  builders.pythonPackage = import ../build/builders/python-package pkgs;

  skimsDependencies = import ../build/src/skims-dependencies.nix pkgs;
in
  pkgs.stdenv.mkDerivation (
       (skimsDependencies.overriden)
    // (rec {
      name = "skims";

      buildInputs = skimsDependencies.runtime;

      pyPkgSkims = builders.pythonPackage {
        cacheKey = ../skims;
        python = pkgs.python38;
        requirement = "skims";
      };
    })
  )
