# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{makePythonPypiEnvironment, ...}:
makePythonPypiEnvironment {
  name = "skims-env-development";
  sourcesYaml = ./pypi-sources.yaml;
}
