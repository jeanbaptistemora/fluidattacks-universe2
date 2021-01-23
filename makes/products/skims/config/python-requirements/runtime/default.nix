{ path
, skimsPkgs
, ...
} @ _:
let
  buildPythonRequirements = import (path "/makes/utils/build-python-requirements") path skimsPkgs;
in
buildPythonRequirements {
  dependencies = [ ];
  requirements = {
    direct = [
      "aioextensions==20.9.2315218"
      "aiofiles==0.5.0"
      "aiogqlc==2.0.0b1"
      "aiohttp==3.6.2"
      "bugsnag==3.8.0"
      "cfn-flip==1.2.3"
      "click==7.1.2"
      "confuse==1.3.0"
      "frozendict==1.2"
      "jmespath==0.10.0"
      "lark-parser==0.7.8"
      "metaloaders==20.9.2566091"
      "more-itertools==8.4.0"
      "networkx==2.5"
      "oyaml==0.9"
      "Pillow==7.2.0"
      "pyparsing==2.4.7"
      "python-dateutil==2.8.1"
      "python-hcl2==0.3.0"
      "python-jose==3.2.0"
      "requests==2.24.0"
      "ruamel.yaml.clib==0.2.2"
      "ruamel.yaml==0.16.10"
      "semver==2.10.2"
      "tree-sitter==0.2.1"
      "uvloop==0.14.0"
    ];
    inherited = [
      "async-timeout==3.0.1"
      "attrs==20.3.0"
      "certifi==2020.12.5"
      "chardet==3.0.4"
      "decorator==4.4.2"
      "ecdsa==0.14.1"
      "idna==2.10"
      "multidict==4.7.6"
      "pyasn1==0.4.8"
      "PyYAML==5.3.1"
      "rsa==4.6"
      "six==1.15.0"
      "urllib3==1.25.11"
      "WebOb==1.8.6"
      "yarl==1.6.3"
    ];
  };
  python = skimsPkgs.python38;
}
