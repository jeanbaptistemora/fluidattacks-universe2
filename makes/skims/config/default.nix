attrs @ {
  outputs,
  pkgsSkims,
  ...
}:

let
  buildPythonRequirements = import ../../../makes/utils/build-python-requirements pkgsSkims;
  makeTemplate = import ../../../makes/utils/make-template pkgsSkims;
in
  rec {
    contextFile = makeTemplate {
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

    osRequirements = rec {
      development = [];
      developmentBinPath = pkgsSkims.lib.strings.makeBinPath development;
      developmentLibPath = pkgsSkims.lib.strings.makeLibraryPath development;

      runtime = [
        pkgsSkims.graphviz
      ];
      runtimeBinPath = pkgsSkims.lib.strings.makeBinPath runtime;
      runtimeLibPath = pkgsSkims.lib.strings.makeLibraryPath runtime;
    };

    pythonRequirements = {
      development = buildPythonRequirements {
        dependencies = [];
        requirements = [
          "astroid==2.4.1"
          "attrs==20.3.0"
          "bandit==1.6.2"
          "coverage==5.3.1"
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
          "mypy==0.790"
          "mypy-extensions==0.4.3"
          "packaging==20.8"
          "pbr==5.5.1"
          "pdoc3==0.8.4"
          "pep8-naming==0.10.0"
          "pluggy==0.13.1"
          "prospector==1.3.0"
          "py==1.10.0"
          "pycodestyle==2.6.0"
          "pydeps==1.9.4"
          "pydocstyle==5.1.1"
          "pyflakes==2.2.0"
          "pylint==2.5.2"
          "pylint-celery==0.3"
          "pylint-django==2.0.15"
          "pylint-flask==0.6"
          "pylint-plugin-utils==0.6"
          "pyparsing==2.4.7"
          "pytest==5.4.3"
          "pytest-asyncio==0.14.0"
          "pytest-cov==2.10.0"
          "pytest-rerunfailures==9.0"
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
        python = pkgsSkims.python38;
      };

      runtime = buildPythonRequirements {
        dependencies = [];
        requirements = [
          "aioextensions==20.9.2315218"
          "aiofiles==0.5.0"
          "aiogqlc==2.0.0b1"
          "aiohttp==3.6.2"
          "async-timeout==3.0.1"
          "attrs==20.3.0"
          "bugsnag==3.8.0"
          "certifi==2020.12.5"
          "cfn-flip==1.2.3"
          "chardet==3.0.4"
          "click==7.1.2"
          "confuse==1.3.0"
          "decorator==4.4.2"
          "ecdsa==0.14.1"
          "frozendict==1.2"
          "idna==2.10"
          "jmespath==0.10.0"
          "lark-parser==0.7.8"
          "metaloaders==20.9.2566091"
          "more-itertools==8.4.0"
          "multidict==4.7.6"
          "networkx==2.5"
          "oyaml==0.9"
          "Pillow==7.2.0"
          "pyasn1==0.4.8"
          "pyparsing==2.4.7"
          "python-dateutil==2.8.1"
          "python-hcl2==0.3.0"
          "python-jose==3.2.0"
          "PyYAML==5.3.1"
          "requests==2.24.0"
          "rsa==4.6"
          "ruamel.yaml==0.16.10"
          "ruamel.yaml.clib==0.2.2"
          "semver==2.10.2"
          "six==1.15.0"
          "urllib3==1.25.11"
          "uvloop==0.14.0"
          "WebOb==1.8.6"
          "yarl==1.6.3"
        ];
        python = pkgsSkims.python38;
      };
    };

    setupSkimsRuntime = makeTemplate {
      arguments = {
        envContextFile = contextFile;
        envPython = "${pkgsSkims.python38}/bin/python";
        envPythonRequirements = pythonRequirements.runtime;
        envRuntimeBinPath = osRequirements.runtimeBinPath;
        envRuntimeLibPath = osRequirements.runtimeLibPath;
        envSrcSkimsSkims = ../../../skims/skims;
        envUtilsBashLibPython = ../../../makes/utils/bash-lib/python.sh;
      };
      name = "skims-config-setup-skims";
      template = ../../../makes/skims/config/setup-skims-runtime.sh;
    };
  }
