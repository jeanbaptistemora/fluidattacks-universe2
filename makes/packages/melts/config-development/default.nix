{ buildPythonRequirements
, makeTemplate
, nixpkgs
, path
, ...
}:
makeTemplate {
  arguments = {
    envPythonRequirements = buildPythonRequirements {
      dependencies = [ ];
      name = "melts-development";
      requirements = {
        direct = [
          "localstack==0.12.5"
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
          "boto3==1.16.56"
          "botocore==1.19.56"
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
      python = nixpkgs.python38;
    };
    envUtilsBashLibPython = path "/makes/utils/python/template.sh";
  };
  name = "melts-config-development";
  searchPaths = {
    envPaths = [
      nixpkgs.docker
    ];
  };
  template = path "/makes/packages/melts/config-development/template.sh";
}
