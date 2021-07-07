{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-target-redshift-runtime-python";
  dependencies = [
    nixpkgs.postgresql
  ];
  requirements = {
    direct = [
      "boto3==1.17.104"
      "click==7.1.2"
      "jsonschema==3.2.0"
      "psycopg2==2.8.4"
      "returns==0.16.0"
    ];
    inherited = [
      "attrs==20.3.0"
      "botocore==1.20.104"
      "importlib-metadata==3.4.0"
      "jmespath==0.10.0"
      "pyrsistent==0.17.3"
      "python-dateutil==2.8.1"
      "s3transfer==0.4.2"
      "six==1.15.0"
      "typing-extensions==3.7.4.3"
      "urllib3==1.26.6"
      "zipp==3.4.0"
    ];
  };
  python = nixpkgs.python38;
}
