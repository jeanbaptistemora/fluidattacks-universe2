let
  pkgs = import ./pkgs.nix { };

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
    firefox
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
    tesseract
    xmlsec
    zlib

    # Python Packages
    #   this is required because this packages depend on shared objects libraries
    _pythonPackages.brotli        # libstdc++.so.6
    _pythonPackages.python_magic  # libmagic.so.1
    _pythonPackages.selenium      # libX11.so.6
  ] ++ basicPythonEnv;

  # Repository files
  srcBuildConfPylintrc = ../build-src/conf/pylintrc;
  srcBuildPythonRequirementsLint = ../build-src/python-requirements/lint.lst;
  srcBuildSh = ../build.sh;
  srcBuildSrc = ../build-src;
  srcBuildSrcConfigPylintrc = ../build-src/config/pylintrc;
  srcBuildSrcPythonRequirementsLint = ../build-src/python-requirements/lint.lst;
  srcBuildSrcPythonRequirementsTest = ../build-src/python-requirements/test.lst;
  srcConfReadmeRst = ../conf/README.rst;
  srcDeploy = ../deploy;
  srcDotGit = builtins.path {
    name = "git";
    path = ../.git;
  };
  srcDotGitShallow = pkgs.stdenv.mkDerivation rec {
    name = "srcDotGitShallow";
    inherit genericDirs genericShellOptions;
    inherit srcGitLastCommitMsg;
    buildInputs = with pkgs; [ git ];
    builder = ./builders/src-dot-git-shallow.sh;
  };
  srcDotMailmap = builtins.path {
    name = "mailmap";
    path = ../.mailmap;
  };
  srcDotOvercommit = builtins.path {
    name = "overcommit.yaml";
    path = ../.overcommit.yml;
  };
  srcDotPreCommitConfig = builtins.path {
    name = "pre-commit-config.yaml";
    path = ../.pre-commit-config.yaml;
  };
  srcEnvrcPublic = builtins.path {
    name = "envrc.public";
    path = ../.envrc.public;
  };
  srcFluidasserts = ../fluidasserts;
  srcGitLastCommitMsg = ../.tmp/git-last-commit-msg;
  srcManifestIn = ../MANIFEST.in;
  srcPackageDotJson = ../package.json;
  srcSetupCfg = ../setup.cfg;
  srcSetupPy = ../setup.py;
  srcSphinx = ../sphinx;
  srcTest = ../test;

  demoFluidassertsOutput = pkgs.stdenv.mkDerivation rec {
    name = "demoFluidassertsOutput";
    description = ''
      Execute fluidasserts over a demo exploit to see the output.
    '';
    inherit genericDirs genericShellOptions;
    inherit pyPkgFluidassertsBasic;
    inherit srcFluidasserts srcTest;
    buildInputs = fluidassertsDeps;
    builder = ./builders/demo-fluidasserts-output.sh;
  };

  fluidassertsDependenciesCache = pkgs.stdenv.mkDerivation rec {
    name = "fluidassertsDependenciesCache";
    description = ''
      Cache of dependencies to build Fluidasserts.
    '';
    inherit genericDirs genericShellOptions;
    inherit srcSetupPy;
    buildInputs = fluidassertsDeps;
    builder = ./builders/fluidasserts-dependencies-cache.sh;
  };

  generateDoc = pkgs.stdenv.mkDerivation rec {
    name = "generateDoc";
    description = ''
      Build the documentation.
    '';
    inherit genericDirs genericShellOptions;
    inherit pyPkgFluidassertsBasic pyPkgGitFame pyPkgSphinx;
    inherit srcDeploy srcDotGit srcDotMailmap srcFluidasserts srcSphinx;
    buildInputs = with pkgs; [
      perl
      fluidassertsDeps
    ];
    builder = ./builders/generate-doc.sh;
  };

  pyPkgFluidassertsBasic = pkgs.stdenv.mkDerivation rec {
    name = "pyPkgFluidassertsBasic";
    description = ''
      Python package for Fluidasserts.

      Not everything needed for a release,
      but what's needed for development purposes.
    '';
    inherit genericDirs genericShellOptions;
    inherit srcConfReadmeRst srcFluidasserts srcManifestIn srcSetupPy;
    inherit fluidassertsDependenciesCache;
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

  pyPkgGroupLint = pkgs.stdenv.mkDerivation rec {
    name = "pyPkgGroupLint";
    description = ''
      Group of Python packages used to lint Fluidasserts.
    '';
    inherit genericDirs genericShellOptions;
    inherit srcBuildSrcPythonRequirementsLint;
    buildInputs = basicPythonEnv;
    builder = ./builders/py-pkg-group-lint.sh;
  };

  pyPkgGroupTest = pkgs.stdenv.mkDerivation rec {
    name = "pyPkgGroupTest";
    description = ''
      Group of Python packages used to test Fluidasserts.
    '';
    inherit genericDirs genericShellOptions;
    inherit srcBuildSrcPythonRequirementsTest;
    buildInputs = basicPythonEnv;
    builder = ./builders/py-pkg-group-test.sh;
  };

  pyPkgSphinx = pkgs.stdenv.mkDerivation rec {
    name = "pyPkgSphinx";
    description = ''
      Python package for Sphinx, with some extensions.
    '';
    inherit genericDirs genericShellOptions;
    inherit pyPkgFluidassertsBasic;
    buildInputs = basicPythonEnv;
    builder = ./builders/py-pkg-sphinx.sh;
  };

  lintFluidassertsCode = pkgs.stdenv.mkDerivation rec {
    name = "lintFluidassertsCode";
    description = ''
      Lint Fluidasserts code.
    '';
    inherit genericDirs genericShellOptions;
    inherit pyPkgFluidassertsBasic pyPkgGroupLint;
    inherit srcBuildSrcConfigPylintrc srcDotGitShallow srcDotOvercommit;
    inherit srcDotPreCommitConfig srcFluidasserts;
    buildInputs = [
      pkgs.haskellPackages.hadolint
      pkgs.overcommit
      pyPkgGroupLint.buildInputs
      fluidassertsDeps
    ];
    builder = ./builders/lint-fluidasserts-code.sh;
  };

  lintFluidassertsTestCode = pkgs.stdenv.mkDerivation rec {
    name = "lintFluidassertsTestCode";
    description = ''
      Lint Fluidasserts test code.
    '';
    inherit genericDirs genericShellOptions;
    inherit pyPkgFluidassertsBasic pyPkgGroupLint;
    inherit srcBuildSrcConfigPylintrc srcDotGitShallow srcDotOvercommit;
    inherit srcDotPreCommitConfig srcTest;
    buildInputs = [
      pkgs.haskellPackages.hadolint
      pkgs.overcommit
      pyPkgGroupLint.buildInputs
      fluidassertsDeps
    ];
    builder = ./builders/lint-fluidasserts-test-code.sh;
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

  lintWithBandit = pkgs.stdenv.mkDerivation rec {
    name = "lintWithBandit";
    description = ''
      Run bandit in fluidasserts code.
    '';
    inherit genericDirs genericShellOptions;
    inherit srcFluidasserts;
    buildInputs = with _pythonPackages; [ bandit ];
    builder = ./builders/lint-with-bandit.sh;
  };

  nodePkgCommitlint = pkgs.stdenv.mkDerivation rec {
    name = "nodePkgCommitlint";
    description = ''
      NodeJS package for Commitlint.
    '';
    inherit genericDirs genericShellOptions;
    inherit srcPackageDotJson;
    buildInputs = with pkgs; [
      cacert
      curl
      nodejs
    ];
    builder = ./builders/node-pkg-commitlint.sh;
  };

  testCommitMessage = pkgs.stdenv.mkDerivation rec {
    name = "testCommitMessage";
    description = ''
      Test the last commit message to ensure an standard format.
    '';
    inherit genericDirs genericShellOptions;
    inherit srcDotGitShallow;
    inherit nodePkgCommitlint;
    buildInputs = with pkgs; [
      git
      nodejs
    ];
    builder = ./builders/test-commit-message.sh;
  };

  testerFluidasserts =
    testGroupName:
      pkgs.stdenv.mkDerivation rec {
        name = testGroupName;
        inherit genericShellOptions;
        inherit srcFluidasserts srcSetupCfg srcTest;
        inherit pyPkgFluidassertsBasic pyPkgGroupTest;
        inherit testGroupName;
        gpg = pkgs.gnupg;
        buildInputs = [
          fluidassertsDeps
          pyPkgGroupTest.buildInputs
        ];
        # Encrypting:
        # echo "${ENCRYPTION_KEY}" \
        #   | gpg --symmetric \
        #         --cipher-algo AES256 \
        #         --digest-algo SHA512 \
        #         --passphrase-fd 0 \
        #         --armor \
        #         --batch \
        #         --yes \
        #       secrets/development.sh
        envVarsEncrypted = ../secrets/development.sh.asc;
        builder = ./builders/tester-fluidasserts.sh;
        runner = ./builders/tester-fluidasserts-runner-script.sh;
      };

  testFluidassertsAll =
    testerFluidasserts "all";

  testFluidassertsCloud =
    testerFluidasserts "cloud";

  testFluidassertsCloudAwsApi =
    testerFluidasserts "cloud.aws.api";

  testFluidassertsCloudAwsCloudformation =
    testerFluidasserts "cloud.aws.cloudformation";

  testFluidassertsCloudAwsTerraform =
    testerFluidasserts "cloud.aws.terraform";

  testFluidassertsCloudAzure =
    testerFluidasserts "cloud.azure";

  testFluidassertsCloudGcp =
    testerFluidasserts "cloud.gcp";

  testFluidassertsCloudKubernetes =
    testerFluidasserts "cloud.kubernetes";

  testFluidassertsDb =
    testerFluidasserts "db";

  testFluidassertsFormat =
    testerFluidasserts "format";

  testFluidassertsHelper =
    testerFluidasserts "helper";

  testFluidassertsIot =
    testerFluidasserts "iot";

  testFluidassertsLangCore =
    testerFluidasserts "lang_core";

  testFluidassertsLangCsharp =
    testerFluidasserts "lang_csharp";

  testFluidassertsLangDocker =
    testerFluidasserts "lang_docker";

  testFluidassertsLangDotnetconfig =
    testerFluidasserts "lang_dotnetconfig";

  testFluidassertsLangHtml =
    testerFluidasserts "lang_html";

  testFluidassertsLangJava =
    testerFluidasserts "lang_java";

  testFluidassertsLangJavascript =
    testerFluidasserts "lang_javascript";

  testFluidassertsLangPhp =
    testerFluidasserts "lang_php";

  testFluidassertsLangPython =
    testerFluidasserts "lang_python";

  testFluidassertsLangRpgle =
    testerFluidasserts "lang_rpgle";

  testFluidassertsLangTimes =
    testerFluidasserts "lang_times";

  testFluidassertsOt =
    testerFluidasserts "ot";

  testFluidassertsProtoDns =
    testerFluidasserts "proto_dns";

  testFluidassertsProtoFtp =
    testerFluidasserts "proto_ftp";

  testFluidassertsProtoGit =
    testerFluidasserts "proto_git";

  testFluidassertsProtoGraphql =
    testerFluidasserts "proto_graphql";

  testFluidassertsProtoHttp =
    testerFluidasserts "proto_http";

  testFluidassertsProtoLdap =
    testerFluidasserts "proto_ldap";

  testFluidassertsProtoRest =
    testerFluidasserts "proto_rest";

  testFluidassertsProtoSmb =
    testerFluidasserts "proto_smb";

  testFluidassertsProtoSmtp =
    testerFluidasserts "proto_smtp";

  testFluidassertsProtoSsh =
    testerFluidasserts "proto_ssh";

  testFluidassertsProtoSsl =
    testerFluidasserts "proto_ssl";

  testFluidassertsProtoTcp =
    testerFluidasserts "proto_tcp";

  testFluidassertsSca =
    testerFluidasserts "sca";

  testFluidassertsSyst =
    testerFluidasserts "syst";

  testFluidassertsUtils =
    testerFluidasserts "utils";

}
