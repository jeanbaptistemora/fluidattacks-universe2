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
    __argScriptGroups__ = projectPath "/makes/foss/units/integrates/back/tools/dump-groups/groups.py";
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
  };
}
