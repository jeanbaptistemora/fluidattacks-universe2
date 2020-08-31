let
  pkgs = import ../pkgs/integrates.nix;
  builders.pythonPackage = import ../builders/python-package pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.sops
        pkgs.jq
        (builders.pythonPackage {}).propagatedBuildInputs
      ];

      pyPkgCryptography = builders.pythonPackage {
        requirement = "cryptography";
      };

      pyPkgMagic = pkgs.python37Packages.magic;
      pyPkgPandas = pkgs.python37Packages.pandas;
      pyPkgNumpy = pkgs.python37Packages.numpy;

      pyPkgIntegratesBack =
        import ../../integrates/django-apps/integrates-back-async pkgs;
    })
  )
