{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-tap-mixpanel-development-python";
  requirements = {
    direct = [
      "boto3==1.17.20"
      "botocore==1.20.20"
      "pytest-freezegun==0.4.2"
      "pytest==6.2.2"
      "ratelimiter==1.2.0"
      "requests==2.25.1"
    ];
    inherited = [
      "attrs==20.3.0"
      "certifi==2020.12.5"
      "chardet==4.0.0"
      "freezegun==1.1.0"
      "idna==2.10"
      "iniconfig==1.1.1"
      "jmespath==0.10.0"
      "numpy==1.20.1"
      "packaging==20.9"
      "pluggy==0.13.1"
      "py==1.10.0"
      "pyparsing==2.4.7"
      "python-dateutil==2.8.1"
      "pytz==2021.1"
      "s3transfer==0.3.4"
      "six==1.15.0"
      "toml==0.10.2"
      "urllib3==1.26.2"
    ];
  };
  python = nixpkgs.python38;
}
