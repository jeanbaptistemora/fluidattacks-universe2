{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-job-last-success-runtime-python";
  requirements = {
    direct = [
      "click==7.1.2"
    ];
    inherited = [ ];
  };
  python = nixpkgs.python38;
}
