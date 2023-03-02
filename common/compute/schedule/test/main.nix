{
  makePythonVersion,
  makeScript,
  outputs,
  projectPath,
  toFileJson,
  ...
}:
makeScript {
  entrypoint = ./entrypoint.sh;
  name = "common-compute-schedule-test";
  replace = {
    __argData__ = toFileJson "data.json" (
      import (projectPath "/common/compute/schedule/data.nix")
    );
    __argSrc__ = ./src/__init__.py;
  };
  searchPaths = {
    bin = [(makePythonVersion "3.10")];
    source = [outputs."/common/compute/schedule/test/env"];
  };
}
