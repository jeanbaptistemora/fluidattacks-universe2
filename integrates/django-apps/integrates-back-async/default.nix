pkgs:

let
  builders.pythonRequirements = import ../../../build/builders/python-requirements pkgs;
in
  pkgs.stdenv.mkDerivation rec {
    name = "integrates-back-async";
    path = ./.;

    propagatedBuildInputs = [
      (pkgs.python37.withPackages (ps: with ps; [
        pip
        setuptools
        wheel
      ]))
    ];

    requirements = builders.pythonRequirements ../../deploy/dependencies/prod-requirements.txt;

    srcIncludeGenericShellOptions = ../../../build/include/generic/shell-options.sh;
    srcIncludeGenericDirStructure = ../../../build/include/generic/dir-structure.sh;

    builder = ./setup.nix.sh;
  }
