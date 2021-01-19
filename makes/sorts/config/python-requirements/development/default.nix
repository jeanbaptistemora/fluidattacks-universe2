{ sortsPkgs
, ...
} @ _:
let
  buildPythonRequirements = import ../../../../../makes/utils/build-python-requirements sortsPkgs;
in
buildPythonRequirements {
  dependencies = [ ];
  requirements = {
    direct = [
      "boto3==1.16.29"
      "numpy==1.19.2"
      "pandas==1.1.2"
      "pytest-cov==2.10.1"
      "pytest-rerunfailures==9.1.1"
      "pytest==6.1.1"
      "sagemaker==2.18.0"
    ];
    inherited = [
      "attrs==20.3.0"
      "botocore==1.19.56"
      "coverage==5.3.1"
      "google-pasta==0.2.0"
      "importlib-metadata==3.4.0"
      "iniconfig==1.1.1"
      "jmespath==0.10.0"
      "packaging==20.8"
      "pluggy==0.13.1"
      "protobuf3-to-dict==0.1.5"
      "protobuf==3.14.0"
      "py==1.10.0"
      "pyparsing==2.4.7"
      "python-dateutil==2.8.1"
      "pytz==2020.5"
      "s3transfer==0.3.4"
      "six==1.15.0"
      "smdebug-rulesconfig==0.1.5"
      "toml==0.10.2"
      "urllib3==1.26.2"
      "zipp==3.4.0"
    ];
  };
  python = sortsPkgs.python38;
}
