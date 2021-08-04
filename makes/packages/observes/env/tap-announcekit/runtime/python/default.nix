{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-tap-announcekit-runtime-python";
  requirements = {
    direct = [
      "click==7.1.2"
      "returns==0.16.0"
      "sgqlc==14.0"
    ];
    inherited = [
      "graphql-core==3.1.5"
      "typing-extensions==3.10.0.0"
    ];
  };
  python = nixpkgs.python38;
}
