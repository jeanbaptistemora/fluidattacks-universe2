# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeTemplate,
  projectPath,
  outputs,
  ...
}:
makeTemplate {
  template = ./entrypoint.sh;
  name = "dump-groups";
  replace = {
    __argScriptGroups__ = projectPath "/integrates/back/tools/dump-groups/groups.py";
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
  };
}
