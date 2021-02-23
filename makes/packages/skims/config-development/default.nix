{ path
, skimsPkgs
, ...
}:
let
  buildPythonRequirements = import (path "/makes/utils/build-python-requirements") path skimsPkgs;
  makeTemplate = import (path "/makes/utils/make-template") path skimsPkgs;
  pythonRequirements = buildPythonRequirements {
    dependencies = [ ];
    name = "skims-development";
    requirements = {
      direct = [
        "bandit==1.6.2"
        "pdoc3==0.8.4"
        "pydeps==1.9.4"
        "pytest-rerunfailures==9.0"
        "pytest==5.4.3"
      ];
      inherited = [
        "attrs==20.3.0"
        "gitdb==4.0.5"
        "GitPython==3.1.12"
        "Mako==1.1.3"
        "Markdown==3.3.3"
        "MarkupSafe==1.1.1"
        "more-itertools==8.6.0"
        "packaging==20.8"
        "pbr==5.5.1"
        "pluggy==0.13.1"
        "py==1.10.0"
        "pyparsing==2.4.7"
        "PyYAML==5.3.1"
        "six==1.15.0"
        "smmap==3.0.4"
        "stdlib-list==0.8.0"
        "stevedore==3.3.0"
        "wcwidth==0.2.5"
      ];
    };
    python = skimsPkgs.python38;
  };
in
makeTemplate {
  arguments = { };
  name = "skims-config-development";
  searchPaths = {
    envPaths = [ pythonRequirements ];
    envPython38Paths = [ pythonRequirements ];
  };
  template = path "/makes/packages/skims/config-development/template.sh";
}
