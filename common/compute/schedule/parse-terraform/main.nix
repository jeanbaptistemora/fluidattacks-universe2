{
  inputs,
  makeTemplate,
  projectPath,
  toFileJson,
  ...
}:
makeTemplate {
  replace = {
    __argParser__ = projectPath "/common/compute/schedule/parse-terraform/src/__init__.py";
    __argSchedules__ = toFileJson "data.json" (
      import (projectPath "/common/compute/schedule/schedules.nix")
    );
  };
  searchPaths.bin = [inputs.nixpkgs.python39];
  template = ./template.sh;
  name = "common-compute-schedule-parse-terraform";
}
