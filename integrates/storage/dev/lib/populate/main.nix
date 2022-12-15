{
  makeTemplate,
  outputs,
  ...
}:
makeTemplate {
  replace = {
    __argData__ = ./data;
  };
  template = ./template.sh;
  name = "integrates-storage-dev-lib-populate";
  searchPaths.source = [
    outputs."/common/utils/aws"
  ];
}
