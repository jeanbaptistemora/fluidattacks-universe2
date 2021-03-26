{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-service-timedoctor-tokens-runtime-python";
  requirements = {
    direct = [
      "click==7.1.2"
    ];
    inherited = [ ];
  };
  python = nixpkgs.python38;
}
