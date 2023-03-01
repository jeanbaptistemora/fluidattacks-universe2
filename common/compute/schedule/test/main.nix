{
  inputs,
  makeScript,
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
  searchPaths.bin = [
    inputs.nixpkgs.python311
    inputs.nixpkgs.yq
  ];
}
