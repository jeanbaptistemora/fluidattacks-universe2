# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
pkgs: let
  builders.pythonRequirements = import ../build/builders/python-requirements pkgs;
in
  pkgs.stdenv.mkDerivation rec {
    name = "asserts";
    path = ./.;

    propagatedBuildInputs = [
      (pkgs.python37.withPackages (ps:
        with ps; [
          setuptools
          pip
        ]))
    ];

    requirements = builders.pythonRequirements ./requirements.txt;

    srcIncludeGenericShellOptions = ../build/include/generic/shell-options.sh;
    srcIncludeGenericDirStructure = ../build/include/generic/dir-structure.sh;

    builder = ./setup.nix.sh;
  }
