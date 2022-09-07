# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{makePythonPypiEnvironment, ...}:
makePythonPypiEnvironment {
  name = "observes-singer-tap-zoho-env-analytics-runtime-python";
  sourcesYaml = ./pypi-sources.yaml;
}
