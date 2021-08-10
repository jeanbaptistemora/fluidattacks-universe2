{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-dev-python";
  requirements = {
    direct = [
      "pytest==6.1.1"
    ];
    inherited = [
      "attrs==21.2.0"
      "iniconfig==1.1.1"
      "packaging==21.0"
      "pluggy==0.13.1"
      "py==1.10.0"
      "pyparsing==2.4.7"
      "toml==0.10.2"
    ];
  };
  python = nixpkgs.python38;
}
