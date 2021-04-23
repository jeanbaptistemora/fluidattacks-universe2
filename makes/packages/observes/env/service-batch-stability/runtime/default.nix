{ buildPythonPackage
, buildPythonRequirements
, makeTemplate
, nixpkgs
, path
, ...
}:
let
  pythonRequirements = buildPythonRequirements {
    name = "observes-env-runtime-batch-stability-python";
    requirements = {
      direct = [
        "boto3==1.17.56"
        "bugsnag==4.0.2"
      ];
      inherited = [
        "botocore==1.20.56"
        "jmespath==0.10.0"
        "python-dateutil==2.8.1"
        "s3transfer==0.4.2"
        "six==1.15.0"
        "urllib3==1.26.4"
        "WebOb==1.8.7"
      ];
    };
    python = nixpkgs.python38;
  };
  self = buildPythonPackage {
    name = "observes-batch-stability";
    packagePath = path "/observes/services/batch_stability";
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "observes-env-runtime-batch-stability";
  searchPaths = {
    envPaths = [
      pythonRequirements
      self
    ];
    envPython38Paths = [
      pythonRequirements
      self
    ];
  };
}
