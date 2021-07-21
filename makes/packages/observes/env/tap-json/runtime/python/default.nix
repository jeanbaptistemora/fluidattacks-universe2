{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-tap-json-runtime-python";
  requirements = {
    direct = [
      "click==8.0.1"
      "dateutils==0.6.12"
      "returns==0.16.0"
    ];
    inherited = [
      "python-dateutil==2.8.1"
      "pytz==2021.1"
      "six==1.16.0"
      "typing-extensions==3.10.0.0"
    ];
  };
  python = nixpkgs.python38;
}
