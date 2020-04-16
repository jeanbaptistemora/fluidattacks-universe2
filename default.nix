pkgs:

let
  builders.pythonRequirements = import ../build/builders/python-requirements pkgs;
in
  pkgs.stdenv.mkDerivation rec {
    name = "fluidattacks";
    path = ./.;

    propagatedBuildInputs = [
      pkgs.python37
      pkgs.python37Packages.pip
      overridenPandas
    ];

    requirements = builders.pythonRequirements ./requirements.txt;
    overridenPandas = pkgs.python3Packages.pandas;

    srcIncludeGenericShellOptions = ../build/include/generic/shell-options.sh;
    srcIncludeGenericDirStructure = ../build/include/generic/dir-structure.sh;

    builder = ./setup.nix.sh;
  }
