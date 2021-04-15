{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-tap-checkly-runtime-python";
  requirements = {
    direct = [
      "click==7.1.2"
      "returns==0.16.0"
    ];
    inherited = [
      "typing-extensions==3.7.4.3"
    ];
  };
  python = nixpkgs.python38;
}
