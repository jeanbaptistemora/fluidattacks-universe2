{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-paginator-runtime-python";
  requirements = {
    direct = [
      "aioextensions==20.11.1621472"
      "Deprecated==1.2.12"
      "returns==0.16.0"
    ];
    inherited = [
      "typing-extensions==3.7.4.3"
      "wrapt==1.12.1"
    ];
  };
  python = nixpkgs.python38;
}
