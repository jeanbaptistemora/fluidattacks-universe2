{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-tap-json-runtime-python";
  requirements = {
    direct = [
      "dateutils==0.6.12"
    ];
    inherited = [
      "python-dateutil==2.8.1"
      "pytz==2021.1"
      "six==1.16.0"
    ];
  };
  python = nixpkgs.python38;
}
