{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-paginator-runtime-python";
  requirements = {
    direct = [
      "aioextensions==20.11.1621472"
      "returns==0.16.0"
    ];
    inherited = [
      "typing-extensions==3.7.4.3"
    ];
  };
  python = nixpkgs.python38;
}
