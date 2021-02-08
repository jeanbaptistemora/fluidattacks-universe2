{ meltsPkgs
, path
, ...
} @ _:
let
  buildPythonRequirements = import (path "/makes/utils/build-python-requirements") path meltsPkgs;
  makeSearchPaths = import (path "/makes/utils/make-search-paths") path meltsPkgs;
  makeTemplate = import (path "/makes/utils/make-template") path meltsPkgs;
in
makeTemplate {
  arguments = {
    envSearchPaths = makeSearchPaths [
      meltsPkgs.git
      meltsPkgs.sops
      meltsPkgs.cloc
      meltsPkgs.networkmanager
      meltsPkgs.openssh
    ];
    envPython = "${meltsPkgs.python38}/bin/python";
    envPythonRequirements = buildPythonRequirements {
      dependencies = [ ];
      name = "melts-runtime";
      requirements = {
        direct = [
          "aioextensions==20.11.1621472"
          "aiogqlc==1.0.3"
          "alive-progress==1.6.1"
          "aws-okta-processor==1.5.0"
          "awscli==1.18.140"
          "binaryornot==0.4.4"
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
          "requests==2.24.0"
          "retry==0.9.2"
          "ruamel.yaml.clib==0.2.2"
          "ruamel.yaml==0.16.10"
          "simplejson==3.17.0"
        ];
        inherited = [
          "aiohttp==3.7.3"
          "async-timeout==3.0.1"
          "attrs==20.3.0"
          "beautifulsoup4==4.9.3"
          "boto3==1.16.56"
          "botocore==1.19.56"
          "bs4==0.0.1"
          "certifi==2020.12.5"
          "chardet==3.0.4"
          "colorama==0.4.3"
          "contextlib2==0.6.0.post1"
          "decorator==4.4.2"
          "docopt==0.6.2"
          "docutils==0.15.2"
          "ecdsa==0.16.1"
          "gitdb==4.0.5"
          "idna==2.10"
          "jmespath==0.10.0"
          "multidict==5.1.0"
          "py==1.10.0"
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
    envSrcMelts = path "/melts";
    envUtilsBashLibPython = path "/makes/utils/python/template.sh";
  };
  name = "melts-config-runtime";
  template = path "/makes/packages/melts/config-runtime/template.sh";
}
