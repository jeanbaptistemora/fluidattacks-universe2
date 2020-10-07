pkgs:

let
  builders.pythonRequirements = import ../build/builders/python-requirements pkgs;
  builders.pythonPackageLocal = import ../build/builders/python-package-local pkgs;
in
  pkgs.stdenv.mkDerivation rec {
    name = "fluidattacks";
    path = ./.;

    propagatedBuildInputs = [
      pkgs.python37
      pkgs.openvpn
      pkgs.python37Packages.pip
      overridenPandas
    ];

    requirements = builders.pythonRequirements ./requirements.txt;
    overridenPandas = pkgs.python3Packages.pandas;

    pyPkgUtilities = builders.pythonPackageLocal {
        path = ../melts/extra-packages/utilities;
        python = pkgs.python37;
    };

    srcIncludeGenericShellOptions = ../build/include/generic/shell-options.sh;
    srcIncludeGenericDirStructure = ../build/include/generic/dir-structure.sh;

    builder = ./setup.nix.sh;
  }
