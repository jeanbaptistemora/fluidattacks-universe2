# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{makePythonPypiEnvironment, ...}:
makePythonPypiEnvironment {
  name = "observes-common-postgres-client-env-type-stubs";
  sourcesYaml = ./pypi-sources.yaml;
}
