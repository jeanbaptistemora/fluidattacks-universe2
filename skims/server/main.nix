{
  makeScript,
  outputs,
  projectPath,
  ...
}:
makeScript {
  name = "skims-serve-report";
  replace = {
    __argSkims__ = projectPath "/skims/skims";
  };
  searchPaths = {
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/env"
      outputs."/skims/config/runtime"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
