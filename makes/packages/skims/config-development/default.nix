{ buildPythonRequirements
, makeTemplate
, path
, nixpkgs
, ...
}:
let
  pythonRequirements = buildPythonRequirements {
    name = "skims-development";
    requirements = {
      direct = [
        "pip-upgrader==1.4.15"
        "pydeps==1.9.4"
        "pytest-rerunfailures==9.0"
        "pytest==5.4.3"
      ];
      inherited = [
        "attrs==20.3.0"
        "certifi==2020.12.5"
        "chardet==4.0.0"
        "colorclass==2.2.0"
        "docopt==0.6.2"
        "idna==2.10"
        "more-itertools==8.7.0"
        "packaging==20.9"
        "pluggy==0.13.1"
        "py==1.10.0"
        "pyparsing==2.4.7"
        "requests==2.25.1"
        "stdlib-list==0.8.0"
        "terminaltables==3.1.0"
        "urllib3==1.26.4"
        "wcwidth==0.2.5"
      ];
    };
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "skims-config-development";
  searchPaths = {
    envPaths = [
      nixpkgs.python38Packages.bandit
      pythonRequirements
    ];
    envPython38Paths = [ pythonRequirements ];
  };
  template = path "/makes/packages/skims/config-development/template.sh";
}
