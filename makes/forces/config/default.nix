{ forcesPkgs
, path
, ...
} @ _:
let
  buildPythonRequirements = import (path "/makes/utils/build-python-requirements") path forcesPkgs;
  makeSearchPaths = import (path "/makes/utils/make-search-paths") path forcesPkgs;
  makeTemplate = import (path "/makes/utils/make-template") path forcesPkgs;
  pythonRequirements = {
    runtime = buildPythonRequirements {
      dependencies = [ ];
      requirements = {
        direct = [
          "aioextensions==20.8.2087641"
          "aiogqlc==2.0.0b1"
          "aiohttp==3.6.2"
          "bugsnag==3.7.1"
          "click==7.1.2"
          "GitPython==3.1.7"
          "more-itertools==8.5.0"
          "oyaml==0.9"
          "python-dateutil==2.8.1"
          "pytz==2020.1"
          "uvloop==0.14.0"
        ];
        inherited = [
          "async-timeout==3.0.1"
          "attrs==20.3.0"
          "chardet==3.0.4"
          "gitdb==4.0.5"
          "idna==3.1"
          "multidict==4.7.6"
          "PyYAML==5.3.1"
          "six==1.15.0"
          "smmap==3.0.4"
          "WebOb==1.8.6"
          "yarl==1.6.3"
        ];
      };
      python = forcesPkgs.python38;
    };
    development = buildPythonRequirements {
      dependencies = [ ];
      requirements = {
        direct = [
          "pytest-asyncio==0.14.0"
          "pytest-cov==2.10.0"
          "pytest==5.4.3"
        ];
        inherited = [
          "attrs==20.3.0"
          "coverage==5.3.1"
          "more-itertools==8.6.0"
          "packaging==20.8"
          "pluggy==0.13.1"
          "py==1.10.0"
          "pyparsing==2.4.7"
          "wcwidth==0.2.5"
        ];
      };
      python = forcesPkgs.python38;
    };
  };
in
{
  setupForcesRuntime = makeTemplate {
    arguments = {
      envSearchPaths = makeSearchPaths [
        forcesPkgs.git
      ];
      envPython = "${forcesPkgs.python38}/bin/python";
      envPythonRequirements = pythonRequirements.runtime;
      envSrcForces = path "/forces";
      envUtilsBashLibPython = path "/makes/utils/bash-lib/python.sh";
    };
    name = "forces-config-setup-forces-runtime";
    template = path "/makes/forces/config/setup-forces-runtime.sh";
  };
  setupForcesDevelopment = makeTemplate {
    arguments = {
      envSearchPaths = makeSearchPaths [ ];
      envPythonRequirements = pythonRequirements.development;
      envUtilsBashLibPython = path "/makes/utils/bash-lib/python.sh";
    };
    name = "forces-config-setup-forces-development";
    template = path "/makes/forces/config/setup-forces-development.sh";
  };
}
