attrs @ {
  outputs,
  skimsPkgs,
  ...
}:

let
  buildPythonRequirements = import ../../../makes/utils/build-python-requirements skimsPkgs;
  makeNixRequirements = inputs: {
    binPath = skimsPkgs.lib.strings.makeBinPath inputs;
    libPath = skimsPkgs.lib.strings.makeLibraryPath inputs;
    pyPath = skimsPkgs.lib.strings.makeSearchPath "lib/python3.8/site-packages" inputs;
  };
  makeTemplate = import ../../../makes/utils/make-template skimsPkgs;
    nixRequirements = builtins.mapAttrs (key: val: makeNixRequirements val) {
      development = [];
      runtime = [
        skimsPkgs.graphviz
        skimsPkgs.python38Packages.pygraphviz
      ];
    };

  pythonRequirements = {
    development = buildPythonRequirements {
      dependencies = [];
      requirements = [
        "astroid==2.4.1"
        "attrs==20.3.0"
        "bandit==1.6.2"  # direct
        "dodgy==0.2.1"
        "flake8==3.8.4"
        "flake8-polyfill==1.0.2"
        "gitdb==4.0.5"
        "GitPython==3.1.11"
        "isort==4.3.21"
        "lazy-object-proxy==1.4.3"
        "Mako==1.1.3"
        "Markdown==3.3.3"
        "MarkupSafe==1.1.1"
        "mccabe==0.6.1"
        "more-itertools==8.6.0"
        "mypy==0.790"  # direct
        "mypy-extensions==0.4.3"  # direct
        "packaging==20.8"
        "pbr==5.5.1"
        "pdoc3==0.8.4"  # direct
        "pep8-naming==0.10.0"
        "pluggy==0.13.1"
        "prospector==1.3.0"  # direct
        "py==1.10.0"
        "pycodestyle==2.6.0"
        "pydeps==1.9.4"  # direct
        "pydocstyle==5.1.1"
        "pyflakes==2.2.0"
        "pylint==2.5.2"
        "pylint-celery==0.3"
        "pylint-django==2.0.15"
        "pylint-flask==0.6"
        "pylint-plugin-utils==0.6"
        "pyparsing==2.4.7"
        "pytest==5.4.3"  # direct
        "pytest-rerunfailures==9.0"  # direct
        "PyYAML==5.3.1"
        "requirements-detector==0.7"
        "setoptconf==0.2.0"
        "six==1.15.0"
        "smmap==3.0.4"
        "snowballstemmer==2.0.0"
        "stdlib-list==0.8.0"
        "stevedore==3.3.0"
        "toml==0.10.2"
        "typed-ast==1.4.1"
        "typing-extensions==3.7.4.3"
        "wcwidth==0.2.5"
        "wrapt==1.12.1"
      ];
      python = skimsPkgs.python38;
    };

    runtime = buildPythonRequirements {
      dependencies = [];
      requirements = [
        "aioextensions==20.9.2315218"  # direct
        "aiofiles==0.5.0"  # direct
        "aiogqlc==2.0.0b1"  # direct
        "aiohttp==3.6.2"  # direct
        "async-timeout==3.0.1"
        "attrs==20.3.0"
        "bugsnag==3.8.0"  # direct
        "certifi==2020.12.5"
        "cfn-flip==1.2.3"  # direct
        "chardet==3.0.4"
        "click==7.1.2"  # direct
        "confuse==1.3.0"  # direct
        "decorator==4.4.2"
        "ecdsa==0.14.1"
        "frozendict==1.2"  # direct
        "idna==2.10"
        "jmespath==0.10.0"  # direct
        "lark-parser==0.7.8"  # direct
        "metaloaders==20.9.2566091"  # direct
        "more-itertools==8.4.0"  # direct
        "multidict==4.7.6"
        "networkx==2.5"  # direct
        "oyaml==0.9"  # direct
        "Pillow==7.2.0"  # direct
        "pyasn1==0.4.8"
        "pyparsing==2.4.7"  # direct
        "python-dateutil==2.8.1"  # direct
        "python-hcl2==0.3.0"  # direct
        "python-jose==3.2.0"  # direct
        "PyYAML==5.3.1"
        "requests==2.24.0"  # direct
        "rsa==4.6"
        "ruamel.yaml==0.16.10"  # direct
        "ruamel.yaml.clib==0.2.2"
        "semver==2.10.2"  # direct
        "six==1.15.0"
        "urllib3==1.25.11"
        "uvloop==0.14.0"  # direct
        "WebOb==1.8.6"
        "yarl==1.6.3"
      ];
      python = skimsPkgs.python38;
    };
  };
in
  {
    setupSkimsDevelopment = makeTemplate {
      arguments = {
        envBinPath = nixRequirements.development.binPath;
        envLibPath = nixRequirements.development.libPath;
        envPyPath = nixRequirements.development.pyPath;
        envPythonRequirements = pythonRequirements.development;
        envUtilsBashLibPython = ../../../makes/utils/bash-lib/python.sh;
      };
      name = "skims-config-setup-skims-development";
      template = ../../../makes/skims/config/setup-skims-development.sh;
    };

    setupSkimsRuntime = makeTemplate {
      arguments = {
        envContextFile = makeTemplate {
          arguments = {
            envParserAntlr = outputs.packages.skims-parsers-antlr;
            envParserBabel = outputs.packages.skims-parsers-babel;
            envSrcSkimsStatic = ../../../skims/static;
            envSrcSkimsVendor = ../../../skims/vendor;
          };
          name = "skims-config-context-file";
          template = ''
            export SKIMS_CIPHER_SUITES_PATH='__envSrcSkimsStatic__/cryptography/cipher_suites.csv'
            export SKIMS_FLUID_WATERMARK='__envSrcSkimsStatic__/img/logo_fluid_attacks_854x329.png'
            export SKIMS_PARSER_ANTLR='__envParserAntlr__/build/install/parse/bin/parse'
            export SKIMS_PARSER_BABEL='__envParserBabel__'
            export SKIMS_ROBOTO_FONT='__envSrcSkimsVendor__/fonts/roboto_mono_from_google/regular.ttf'
            export SKIMS_STATIC='__envSrcSkimsStatic__'
            export SKIMS_VENDOR='__envSrcSkimsVendor__'
          '';
        };
        envPython = "${skimsPkgs.python38}/bin/python";
        envPythonRequirements = pythonRequirements.runtime;
        envBinPath = nixRequirements.runtime.binPath;
        envLibPath = nixRequirements.runtime.libPath;
        envPyPath = nixRequirements.runtime.pyPath;
        envSrcSkimsSkims = ../../../skims/skims;
        envUtilsBashLibPython = ../../../makes/utils/bash-lib/python.sh;
      };
      name = "skims-config-setup-skims-runtime";
      template = ../../../makes/skims/config/setup-skims-runtime.sh;
    };
  }
