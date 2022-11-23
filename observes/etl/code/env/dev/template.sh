# shellcheck shell=bash

mkdir -p ./.vscode \
  && "__argPython__" "__argPythonEntry__" ./.vscode/settings.json "__argPythonEnv__"
