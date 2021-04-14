{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-tap-mixpanel-development-python";
  requirements = {
    direct = [
      "pytest-freezegun==0.4.2"
      "pytest==6.2.2"
    ];
    inherited = [
      "attrs==20.3.0"
      "freezegun==1.1.0"
      "iniconfig==1.1.1"
      "packaging==20.9"
      "pluggy==0.13.1"
      "py==1.10.0"
      "pyparsing==2.4.7"
      "python-dateutil==2.8.1"
      "six==1.15.0"
      "toml==0.10.2"
    ];
  };
  python = nixpkgs.python38;
}
