let
  pkgs = import ./pkgs.nix;

  _python = pkgs.python37;
  _pythonPackages = pkgs.python37Packages;
in

rec {
  # sourceable files to set an standard dir structure and predefined shell options
  genericDirs = ./include/generic/dirs.sh;
  genericShellOptions = ./include/generic/shell-options.sh;

  # A list of packages to provide a basic python environment
  basicPythonEnv = [
    (_pythonPackages.pip)
    (_python.withPackages (ps: with ps; [ cython setuptools wheel ]))
  ];

  # Fluidasserts dependencies
  fluidassertsDeps = with pkgs; [
    # OS dependencies
    autoconf
    binutils
    brotli
    cacert
    cmake
    freetds
    freetype
    gcc
    git
    lcms2
    libffi
    libjpeg
    libwebp
    libxml2
    libxslt
    openssl
    postgresql
    xmlsec
    zlib

    # Python Packages
    #   this is required because this packages depend on shared objects libraries
    _pythonPackages.brotli        # libstdc++.so.6
    _pythonPackages.python_magic  # libmagic.so.1
  ] ++ basicPythonEnv;

  # Repository files
  srcBuildConfPylintrc = ../build-src/conf/pylintrc;
  srcBuildPythonRequirementsLint = ../build-src/python-requirements/lint.lst;
  srcBuildSh = ../build.sh;
  srcBuildSrc = ../build-src;
  srcConfReadmeRst = ../conf/README.rst;
  srcDeploy = ../deploy;
  srcDotGit = builtins.path {
    name = "git";
    path = ../.git;
  };
  srcEnvrcPublic = builtins.path {
    name = "envrc.public";
    path = ../.envrc.public;
  };
  srcFluidasserts = ../fluidasserts;
  srcManifestIn = ../MANIFEST.in;
  srcSetupPy = ../setup.py;
  srcSphinx = ../sphinx;
  srcTest = ../test;

  demoFluidassertsOutput = pkgs.stdenv.mkDerivation rec {
    name = "demoFluidassertsOutput";
    description = ''
      Execute fluidasserts over a demo exploit to see the output.
    '';
    inherit genericDirs genericShellOptions;
    inherit pyPkgFluidasserts;
    inherit srcFluidasserts srcTest;
    buildInputs = fluidassertsDeps;
    builder = ./builders/demo-fluidasserts-output.sh;
  };

  generateDoc = pkgs.stdenv.mkDerivation rec {
    name = "generateDoc";
    description = ''
      Build the documentation.
    '';
    inherit genericDirs genericShellOptions;
    inherit pyPkgFluidasserts pyPkgGitFame pyPkgSphinx;
    inherit srcDeploy srcDotGit srcFluidasserts srcSphinx;
    buildInputs = with pkgs; [
      perl
    ] ++ fluidassertsDeps;
    builder = ./builders/generate-doc.sh;
  };

  pyPkgFluidasserts = pkgs.stdenv.mkDerivation rec {
    name = "pyPkgFluidasserts";
    description = ''
      Python package for Fluidasserts.
    '';
    inherit genericDirs genericShellOptions;
    inherit srcConfReadmeRst srcFluidasserts srcManifestIn srcSetupPy srcTest;
    buildInputs = fluidassertsDeps;
    builder = ./builders/py-pkg-fluidasserts.sh;
  };

  pyPkgGitFame = pkgs.stdenv.mkDerivation rec {
    name = "pyPkgGitFame";
    description = ''
      Python package for git-fame.
    '';
    inherit genericDirs genericShellOptions;
    buildInputs = basicPythonEnv;
    builder = ./builders/py-pkg-git-fame.sh;
  };

  pyPkgSphinx = pkgs.stdenv.mkDerivation rec {
    name = "pyPkgSphinx";
    description = ''
      Python package for Sphinx, with some extensions.
    '';
    inherit genericDirs genericShellOptions;
    inherit pyPkgFluidasserts;
    buildInputs = basicPythonEnv;
    builder = ./builders/py-pkg-sphinx.sh;
  };

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
