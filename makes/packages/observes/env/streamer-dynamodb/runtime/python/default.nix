{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-streamer-dynamodb-runtime-python";
  requirements = {
    direct = [
      "aioboto3==8.0.5"
      "aioextensions==20.8.2087641"
      "aiomultiprocess==0.8.0"
    ];
    inherited = [
      "aiobotocore==1.0.4"
      "aiohttp==3.7.3"
      "aioitertools==0.7.1"
      "async-timeout==3.0.1"
      "attrs==20.3.0"
      "boto3==1.12.32"
      "botocore==1.15.32"
      "chardet==3.0.4"
      "docutils==0.15.2"
      "idna==3.1"
      "jmespath==0.10.0"
      "multidict==5.1.0"
      "python-dateutil==2.8.1"
      "s3transfer==0.3.4"
      "six==1.15.0"
      "typing-extensions==3.7.4.3"
      "urllib3==1.25.11"
      "uvloop==0.15.1"
      "wrapt==1.12.1"
      "yarl==1.6.3"
    ];
  };
  python = nixpkgs.python38;
}
