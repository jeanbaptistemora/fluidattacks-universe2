let
  pkgs = import ../build/pkgs/stable.nix;

  builders.pythonPackage = import ../build/builders/python-package pkgs;
  builders.pythonPackageLocal = import ../build/builders/python-package-local pkgs;
in
  pkgs.stdenv.mkDerivation rec {
    name = "bin";

    buildInputs = [
    ];

    pyPkgFluidasserts = builders.pythonPackage {
      requirement = "fluidasserts==20.7.21401";
      dependencies = [
        pkgs.postgresql
        pkgs.unixODBC
      ];
    };

    pyPkgSkims = builders.pythonPackageLocal ../skims;
  }
