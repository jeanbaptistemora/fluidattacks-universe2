{ buildPythonRequirements
, nixpkgs
, ...
}:
buildPythonRequirements {
  name = "observes-env-gitlab-etl-development-python";
  requirements = {
    direct = [
      "pytest-asyncio==0.14.0"
      "pytest-timeout==1.4.2"
      "pytest==6.1.1"
    ];
    inherited = [
      "attrs==21.2.0"
      "iniconfig==1.1.1"
      "packaging==20.9"
      "pluggy==0.13.1"
      "py==1.10.0"
      "pyparsing==2.4.7"
      "toml==0.10.2"
    ];
  };
  python = nixpkgs.python38;
}
