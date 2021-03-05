{ nixpkgs2
, path
, ...
}:
let
  buildPythonRequirements = import (path "/makes/utils/build-python-requirements") path nixpkgs2;
in
buildPythonRequirements {
  dependencies = [ ];
  name = "integrates-web-e2e-pypi";
  requirements = {
    direct = [
      "itsdangerous==1.1.0"
      "pytest-rerunfailures==9.1.1"
      "pytest-test-groups==1.0.3"
      "pytest==6.1.2"
      "selenium==3.141.0"
    ];
    inherited = [
      "attrs==20.3.0"
      "iniconfig==1.1.1"
      "packaging==20.9"
      "pluggy==0.13.1"
      "py==1.10.0"
      "pyparsing==2.4.7"
      "toml==0.10.2"
      "urllib3==1.26.3"
    ];
  };
  python = nixpkgs2.python38;
}
