{ buildPythonRequirements
, makeTemplate
, nixpkgs
, packages
, ...
}:
let
  pythonRequirements = buildPythonRequirements {
    name = "integrates-back-unit-tests";
    requirements = {
      direct = [
        "aniso8601==9.0.0"
        "freezegun==0.3.15"
        "moto[secretsmanager]==1.3.16"
        "pytest-asyncio==0.12.0"
        "pytest-cov==2.9.0"
        "pytest==5.4.1"
        "selenium==3.141.0"
      ];
      inherited = [
        "attrs==20.3.0"
        "aws-sam-translator==1.35.0"
        "aws-xray-sdk==2.7.0"
        "boto3==1.17.57"
        "boto==2.49.0"
        "botocore==1.20.57"
        "certifi==2020.12.5"
        "cffi==1.14.5"
        "cfn-lint==0.48.3"
        "chardet==4.0.0"
        "coverage==5.5"
        "cryptography==3.4.7"
        "decorator==4.4.2"
        "docker==5.0.0"
        "ecdsa==0.14.1"
        "future==0.18.2"
        "idna==2.10"
        "importlib-metadata==4.0.1"
        "Jinja2==2.11.3"
        "jmespath==0.10.0"
        "jsondiff==1.3.0"
        "jsonpatch==1.32"
        "jsonpointer==2.1"
        "jsonschema==3.2.0"
        "junit-xml==1.9"
        "MarkupSafe==1.1.1"
        "mock==4.0.3"
        "more-itertools==8.7.0"
        "networkx==2.5.1"
        "packaging==20.9"
        "pluggy==0.13.1"
        "py==1.10.0"
        "pyasn1==0.4.8"
        "pycparser==2.20"
        "pyparsing==2.4.7"
        "pyrsistent==0.17.3"
        "python-dateutil==2.8.1"
        "python-jose==3.2.0"
        "pytz==2021.1"
        "PyYAML==5.4.1"
        "requests==2.25.1"
        "responses==0.13.2"
        "rsa==4.7.2"
        "s3transfer==0.4.2"
        "six==1.15.0"
        "sshpubkeys==3.3.1"
        "typing-extensions==3.7.4.3"
        "urllib3==1.26.4"
        "wcwidth==0.2.5"
        "websocket-client==0.58.0"
        "Werkzeug==1.0.1"
        "wrapt==1.12.1"
        "xmltodict==0.12.0"
        "zipp==3.4.1"
      ];
    };
    python = nixpkgs.python37;
  };
in
makeTemplate {
  name = "integrates-back-pypi-unit-tests";
  searchPaths = {
    envPaths = [
      packages.integrates.cache
      packages.integrates.db
      packages.integrates.storage
      pythonRequirements
    ];
    envPython37Paths = [
      pythonRequirements
    ];
  };
}
