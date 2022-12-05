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
  searchPaths = {
    bin = [
      outputs."/deployTerraform/integratesStorageDev"
    ];
    source = [
      outputs."/common/utils/aws"
    ];
  };
}
