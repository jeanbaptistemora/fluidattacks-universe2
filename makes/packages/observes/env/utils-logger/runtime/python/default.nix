{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-utils-logger-runtime-python";
  requirements = {
    direct = [
      "bugsnag==4.0.2"
    ];
    inherited = [
      "WebOb==1.8.7"
    ];
  };
  python = nixpkgs.python38;
}
