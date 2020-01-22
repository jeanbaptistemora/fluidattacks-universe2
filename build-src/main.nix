let
  pkgs = import ./pkgs.nix;
in

rec {
  # sourceable files to set an standard dir structure and predefined shell options
  genericDirs = ./include/generic/dirs.sh;
  genericShellOptions = ./include/generic/shell-options.sh;

  # The basic python binary
  _python = pkgs.python3.withPackages (ps: with ps; [
    cython
    setuptools
    wheel
  ]);

  # Repository files
  srcBuildConfPylintrc = ../build-src/conf/pylintrc;
  srcBuildPythonRequirementsLint = ../build-src/python-requirements/lint.lst;
  srcBuildSh = ../build.sh;
  srcBuildSrc = ../build-src;
  srcEnvrcPublic = builtins.path {
    name = "envrc.public";
    path = ../.envrc.public;
  };
  srcFluidasserts = ../fluidasserts;

  lintNixCode = pkgs.stdenv.mkDerivation rec {
    name = "lintNixCode";
    description = ''
      Lint Nix(pkgs) code in the repository.
    '';
    inherit genericDirs genericShellOptions;
    inherit srcBuildSrc;
    buildInputs = with pkgs; [ nix-linter ];
    builder = ./builders/lint-nix-code.sh;
  };

  lintPythonCodeBandit = pkgs.stdenv.mkDerivation rec {
    name = "lintPythonCodeBandit";
    description = ''
      Run bandit in fluidasserts code.
    '';
    inherit genericDirs genericShellOptions;
    inherit srcFluidasserts;
    buildInputs = with pkgs; with python3Packages; [ bandit ];
    builder = ./builders/lint-python-code-bandit.sh;
  };

  lintShellCode = pkgs.stdenv.mkDerivation rec {
    name = "lintShellCode";
    description = ''
      Lint shell code in the repository.
    '';
    inherit genericDirs genericShellOptions;
    inherit srcBuildSh srcBuildSrc srcEnvrcPublic;
    buildInputs = with pkgs; [ shellcheck ];
    builder = ./builders/lint-shell-code.sh;
  };
}
