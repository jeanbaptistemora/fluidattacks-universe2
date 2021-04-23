{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-streamer-dynamodb-runtime-python";
  requirements = {
    direct = [
      "aioboto3==8.3.0"
      "aioextensions==20.11.1621472"
      "aiomultiprocess==0.9.0"
    ];
    inherited = [
      "aiobotocore==1.2.2"
      "aiohttp==3.7.4.post0"
      "aioitertools==0.7.1"
      "async-timeout==3.0.1"
      "attrs==20.3.0"
      "boto3==1.16.52"
      "botocore==1.19.52"
      "chardet==4.0.0"
      "idna==3.1"
      "jmespath==0.10.0"
      "multidict==5.1.0"
      "python-dateutil==2.8.1"
      "s3transfer==0.3.7"
      "six==1.15.0"
      "typing-extensions==3.7.4.3"
      "urllib3==1.26.4"
      "wrapt==1.12.1"
      "yarl==1.6.3"
    ];
  };
  python = nixpkgs.python38;
}
