# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

mkdir -p ./.vscode \
  && "__argPython__" "__argPythonEntry__" ./.vscode/settings.json "__argPythonEnv__"
