{
  makeScript,
  outputs,
  ...
}:
makeScript {
  replace = {
    __argData__ = ./data;
  };
  entrypoint = ./entrypoint.sh;
  name = "integrates-storage-dev";
  searchPaths = {
    bin = [
      outputs."/deployTerraform/integratesStorageDev"
    ];
    source = [
      outputs."/common/utils/aws"
    ];
  };
}
