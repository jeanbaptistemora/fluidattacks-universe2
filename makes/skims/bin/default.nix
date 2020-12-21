attrs @ {
  pkgsSkims,
  ...
}:

let
  buildPythonRequirements = import ../../../makes/utils/build-python-requirements pkgsSkims;
  makeApp = import ../../../makes/utils/make-app pkgsSkims;
in
  makeApp {
    arguments = {
      envANTLR = import ../../../makes/skims/parsers/antlr {
        inherit pkgsSkims;
      };
      envShell = "${pkgsSkims.bash}/bin/bash";
      envPython = "${pkgsSkims.python38}/bin/python";
      envPythonRequirements = buildPythonRequirements {
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
      envSrcSkimsSkims = ../../../skims/skims;
      envSrcSkimsStatic = ../../../skims/static;
      envSrcSkimsVendor = ../../../skims/vendor;
    };
    name = "skims-bin";
    template = ../../../makes/skims/bin/entrypoint.sh;
  }
