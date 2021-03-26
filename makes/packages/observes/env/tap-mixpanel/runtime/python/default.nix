{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-tap-mixpanel-runtime-python";
  requirements = {
    direct = [
      "boto3==1.17.20"
      "botocore==1.20.20"
      "ratelimiter==1.2.0"
      "requests==2.25.1"
    ];
    inherited = [
      "certifi==2020.12.5"
      "chardet==4.0.0"
      "idna==2.10"
      "jmespath==0.10.0"
      "numpy==1.20.1"
      "python-dateutil==2.8.1"
      "pytz==2021.1"
      "s3transfer==0.3.4"
      "six==1.15.0"
      "urllib3==1.26.2"
    ];
  };
  python = nixpkgs.python38;
}
