{ meltsPkgs
, ...
} @ _:
let
  buildPythonRequirements = import ../../../makes/utils/build-python-requirements meltsPkgs;
  makeSearchPaths = import ../../../makes/utils/make-search-paths meltsPkgs;
  makeTemplate = import ../../../makes/utils/make-template meltsPkgs;
  nixRequirements = {
    development = makeSearchPaths [ ];
    runtime = makeSearchPaths [ ];
  };

  pythonRequirements = {
    runtime = buildPythonRequirements {
      dependencies = [ ];
      requirements = {
        direct = [
          "aiogqlc==1.0.3"
          "alive-progress==1.6.1"
          "aws-okta-processor==1.5.0"
          "awscli==1.18.40"
          "binaryornot==0.4.4"
          "boto3==1.12.40"
          "botocore==1.15.40"
          "bugsnag==3.7.1"
          "click==7.1.2"
          "frozendict==1.2"
          "GitPython==3.1.11"
          "more-itertools==8.5.0"
          "mypy-extensions==0.4.3"
          "pathspec==0.8.1"
          "pykwalify==1.7.0"
          "pynamodb==4.3.1"
          "python-dateutil==2.8.1"
          "python-git==2018.2.1"
          "python-jose==3.1.0"
          "pytz==2020.4"
          "requests==2.23.0"
          "ruamel.yaml.clib==0.2.2"
          "ruamel.yaml==0.16.10"
          "simplejson==3.17.0"
        ];
        inherited = [
          "aiohttp==3.7.3"
          "async-timeout==3.0.1"
          "attrs==20.3.0"
          "beautifulsoup4==4.9.3"
          "bs4==0.0.1"
          "certifi==2020.12.5"
          "chardet==4.0.0"
          "colorama==0.4.3"
          "contextlib2==0.6.0.post1"
          "docopt==0.6.2"
          "docutils==0.15.2"
          "ecdsa==0.16.1"
          "gitdb==4.0.5"
          "idna==2.10"
          "jmespath==0.10.0"
          "multidict==5.1.0"
          "pyasn1==0.4.8"
          "PyYAML==5.3.1"
          "rsa==3.4.2"
          "s3transfer==0.3.3"
          "Send2Trash==1.5.0"
          "six==1.15.0"
          "smmap==3.0.4"
          "soupsieve==2.1"
          "typing-extensions==3.7.4.3"
          "urllib3==1.25.11"
          "WebOb==1.8.6"
          "yarl==1.6.3"
        ];
      };
      python = meltsPkgs.python38;
    };
    development = buildPythonRequirements {
      dependencies = [ ];
      requirements = {
        direct = [
          "localstack==0.11.0.5"
          "pytest-cov==2.7.1"
          "pytest-random-order==1.0.4"
          "pytest-rerunfailures==9.0"
          "pytest-xdist==1.29.0"
          "pytest==5.1.2"
        ];
        inherited = [
          "apipkg==1.5"
          "atomicwrites==1.4.0"
          "attrs==20.3.0"
          "boto3==1.16.55"
          "botocore==1.19.55"
          "certifi==2020.12.5"
          "chardet==4.0.0"
          "coverage==5.3.1"
          "dnslib==0.9.14"
          "dnspython==1.16.0"
          "docopt==0.6.2"
          "execnet==1.7.1"
          "idna==2.10"
          "jmespath==0.10.0"
          "localstack-client==1.10"
          "localstack-ext==0.12.4.9"
          "more-itertools==8.6.0"
          "packaging==20.8"
          "pluggy==0.13.1"
          "py==1.10.0"
          "pyaes==1.6.1"
          "pyparsing==2.4.7"
          "pytest-forked==1.3.0"
          "python-dateutil==2.8.1"
          "requests==2.25.1"
          "s3transfer==0.3.4"
          "six==1.15.0"
          "subprocess32==3.5.4"
          "urllib3==1.26.2"
          "wcwidth==0.2.5"
        ];
      };
      python = meltsPkgs.python38;
    };
  };
in
{
  setupMeltsRuntime = makeTemplate {
    arguments = {
      envBinPath = nixRequirements.runtime.binPath;
      envLibPath = nixRequirements.runtime.libPath;
      envPyPath = nixRequirements.runtime.pyPath;
      envPython = "${meltsPkgs.python38}/bin/python";
      envPythonRequirements = pythonRequirements.runtime;
      envSrcMelts = ../../../melts;
      envUtilsBashLibPython = ../../../makes/utils/bash-lib/python.sh;
    };
    name = "melts-config-setup-melts-runtime";
    template = ../../../makes/melts/config/setup-melts-runtime.sh;
  };
  setupMeltsDevelopment = makeTemplate {
    arguments = {
      envBinPath = nixRequirements.development.binPath;
      envLibPath = nixRequirements.development.libPath;
      envPyPath = nixRequirements.development.pyPath;
      envPythonRequirements = pythonRequirements.development;
      envUtilsBashLibPython = ../../../makes/utils/bash-lib/python.sh;
    };
    name = "melts-config-setup-melts-development";
    template = ../../../makes/melts/config/setup-melts-development.sh;
  };
}
