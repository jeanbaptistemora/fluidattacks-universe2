path: pkgs:
let
  buildPythonRequirements = import (path "/makes/utils/build-python-requirements") path pkgs;
  makeTemplate = import (path "/makes/utils/make-template") path pkgs;
in
makeTemplate {
  arguments = {
    envPythonRequirements = buildPythonRequirements {
      dependencies = [ ];
      name = "lint-python";
      requirements = {
        direct = [
          "import-linter==1.2"
          "mypy==0.790"
          "prospector==1.3.0"
        ];
        inherited = [
          "astroid==2.4.1"
          "click==7.1.2"
          "decorator==4.4.2"
          "dodgy==0.2.1"
          "flake8-polyfill==1.0.2"
          "flake8==3.8.4"
          "grimp==1.2.2"
          "isort==4.3.21"
          "lazy-object-proxy==1.4.3"
          "mccabe==0.6.1"
          "mypy-extensions==0.4.3"
          "networkx==2.5"
          "pep8-naming==0.10.0"
          "pycodestyle==2.6.0"
          "pydocstyle==5.1.1"
          "pyflakes==2.2.0"
          "pylint-celery==0.3"
          "pylint-django==2.0.15"
          "pylint-flask==0.6"
          "pylint-plugin-utils==0.6"
          "pylint==2.5.2"
          "PyYAML==5.3.1"
          "requirements-detector==0.7"
          "setoptconf==0.2.0"
          "six==1.15.0"
          "snowballstemmer==2.0.0"
          "toml==0.10.2"
          "typed-ast==1.4.2"
          "typing-extensions==3.7.4.3"
          "wrapt==1.12.1"
        ];
      };
      python = pkgs.python38;
    };
    envSettingsMypy = path "/makes/utils/lint-python/settings-mypy.cfg";
    envSettingsProspector = path "/makes/utils/lint-python/settings-prospector.yaml";
    envUtilsBashLibPython = path "/makes/utils/python/template.sh";
  };
  name = "utils-bash-lib-lint-python";
  template = path "/makes/utils/lint-python/template.sh";
}
