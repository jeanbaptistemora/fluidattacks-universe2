{
  inputs,
  makePythonVersion,
  makeScript,
  outputs,
  projectPath,
  ...
}:
makeScript {
  entrypoint = ./entrypoint.sh;
  name = "common-compute-schedule-test";
  replace = {
    __argData__ = projectPath "/common/compute/schedule/data.yaml";
    __argSrc__ = ./src/__init__.py;
  };
  searchPaths = {
    bin = [
      (makePythonVersion "3.10")
      inputs.nixpkgs.yq
    ];
    source = [outputs."/common/compute/schedule/test/env"];
  };
}
