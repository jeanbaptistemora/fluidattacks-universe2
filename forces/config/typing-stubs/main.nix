# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{makePythonPypiEnvironment, ...}:
makePythonPypiEnvironment {
  name = "forces-config-typing-stubs";
  sourcesYaml = ./pypi-sources.yaml;
}
