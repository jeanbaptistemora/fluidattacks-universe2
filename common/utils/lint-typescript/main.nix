{
  makeTemplate,
  projectPath,
  ...
}:
makeTemplate {
  replace = {
    __argConfig__ = projectPath "/common/utils/lint-typescript";
  };
  name = "utils-bash-lib-lint-typescript";
  template = ./template.sh;
}
