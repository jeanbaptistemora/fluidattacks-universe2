{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-service-jobs-scheduler-runtime-python";
  requirements = {
    direct = [
      "returns==0.16.0"
    ];
    inherited = [
      "typing-extensions==3.10.0.0"
    ];
  };
  python = nixpkgs.python38;
}
