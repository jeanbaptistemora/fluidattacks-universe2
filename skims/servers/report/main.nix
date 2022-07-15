{
  makeScript,
  makePythonVersion,
  outputs,
  projectPath,
  ...
}:
makeScript {
  name = "skims-serve-report";
  replace = {
    __argServer__ = projectPath "/skims/servers/report";
  };
  searchPaths = {
    bin = [
      (makePythonVersion "3.9")
    ];
    source = [
      outputs."/skims/servers/report/env"
      outputs."/common/utils/env"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
