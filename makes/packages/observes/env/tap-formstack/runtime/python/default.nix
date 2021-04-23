{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-tap-formstack-runtime-python";
  requirements = {
    direct = [
      "python-dateutil==2.8.1"
      "requests==2.25.1"
    ];
    inherited = [
      "certifi==2020.12.5"
      "chardet==4.0.0"
      "idna==2.10"
      "six==1.15.0"
      "urllib3==1.26.4"
    ];
  };
  python = nixpkgs.python38;
}
