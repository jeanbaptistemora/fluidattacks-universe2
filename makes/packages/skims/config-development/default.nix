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
        "pdoc3==0.8.4"
        "pydeps==1.9.4"
        "pytest-rerunfailures==9.0"
        "pytest==5.4.3"
      ];
      inherited = [
        "attrs==20.3.0"
        "Mako==1.1.3"
        "Markdown==3.3.3"
        "MarkupSafe==1.1.1"
        "more-itertools==8.6.0"
        "packaging==20.8"
        "pluggy==0.13.1"
        "py==1.10.0"
        "pyparsing==2.4.7"
        "stdlib-list==0.8.0"
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
