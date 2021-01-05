_ @ {
  skimsPkgs,
  ...
}:

let
  buildPythonRequirements = import ../../../../../makes/utils/build-python-requirements skimsPkgs;
in
  buildPythonRequirements {
    dependencies = [];
    requirements = {
      direct = [
        "bandit==1.6.2"
        "mypy-extensions==0.4.3"
        "mypy==0.790"
        "pdoc3==0.8.4"
        "prospector==1.3.0"
        "pydeps==1.9.4"
        "pytest-rerunfailures==9.0"
        "pytest==5.4.3"
      ];
      inherited = [
        "astroid==2.4.1"
        "attrs==20.3.0"
        "dodgy==0.2.1"
        "flake8-polyfill==1.0.2"
        "flake8==3.8.4"
        "gitdb==4.0.5"
        "GitPython==3.1.11"
        "isort==4.3.21"
        "lazy-object-proxy==1.4.3"
        "Mako==1.1.3"
        "Markdown==3.3.3"
        "MarkupSafe==1.1.1"
        "mccabe==0.6.1"
        "more-itertools==8.6.0"
        "packaging==20.8"
        "pbr==5.5.1"
        "pep8-naming==0.10.0"
        "pluggy==0.13.1"
        "py==1.10.0"
        "pycodestyle==2.6.0"
        "pydocstyle==5.1.1"
        "pyflakes==2.2.0"
        "pylint-celery==0.3"
        "pylint-django==2.0.15"
        "pylint-flask==0.6"
        "pylint-plugin-utils==0.6"
        "pylint==2.5.2"
        "pyparsing==2.4.7"
        "PyYAML==5.3.1"
        "requirements-detector==0.7"
        "setoptconf==0.2.0"
        "six==1.15.0"
        "smmap==3.0.4"
        "snowballstemmer==2.0.0"
        "stdlib-list==0.8.0"
        "stevedore==3.3.0"
        "toml==0.10.2"
        "typed-ast==1.4.1"
        "typing-extensions==3.7.4.3"
        "wcwidth==0.2.5"
        "wrapt==1.12.1"
      ];
    };
    python = skimsPkgs.python38;
  }
