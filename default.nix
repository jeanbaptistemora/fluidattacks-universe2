pkgs:

let
  builders.pythonRequirements = import build2/builders/python-requirements pkgs;
in
  pkgs.stdenv.mkDerivation rec {
    name = "asserts";
    path = ./.;

    propagatedBuildInputs = [
      (pkgs.python37.withPackages (ps: with ps; [
        setuptools
        pip
      ]))
    ];

    requirements = builders.pythonRequirements ./requirements.txt;

    srcIncludeGenericShellOptions = build2/include/generic/shell-options.sh;
    srcIncludeGenericDirStructure = build2/include/generic/dir-structure.sh;

    builder = ./setup.nix.sh;
  }
