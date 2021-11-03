{ makeTemplate
, projectPath
, ...
}:
makeTemplate {
  replace = {
    __argConfig__ = projectPath "/makes/foss/units/utils/lint-typescript";
  };
  name = "utils-bash-lib-lint-typescript";
  template = ./template.sh;
}
