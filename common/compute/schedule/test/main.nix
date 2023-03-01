{
  inputs,
  makeScript,
  projectPath,
  toFileJson,
  ...
}:
makeScript {
  entrypoint = ./entrypoint.sh;
  name = "common-compute-schedule-test";
  replace = {
    __argSchedules__ = toFileJson "data.json" (
      import (projectPath "/common/compute/schedule/schedules.nix")
    );
    __argSrc__ = ./src/__init__.py;
  };
  searchPaths.bin = [inputs.nixpkgs.python311];
}
