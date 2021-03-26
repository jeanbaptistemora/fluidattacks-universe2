{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-service-migrate-tables-runtime-python";
  requirements = {
    direct = [
      "click==7.1.2"
    ];
    inherited = [ ];
  };
  python = nixpkgs.python38;
}
