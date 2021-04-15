{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-paginator-runtime-python";
  requirements = {
    direct = [
      "aioextensions==20.11.1621472"
    ];
    inherited = [ ];
  };
  python = nixpkgs.python38;
}
