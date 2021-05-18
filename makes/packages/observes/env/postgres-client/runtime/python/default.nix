{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-postgres-client-runtime-python";
  requirements = {
    direct = [
      "returns==0.16.0"
    ];
    inherited = [
      "typing-extensions==3.7.4.3"
    ];
  };
  python = nixpkgs.python38;
}
