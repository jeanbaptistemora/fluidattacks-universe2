# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
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
    __argSizes__ = projectPath "/common/compute/arch/sizes/data.yaml";
  };
  searchPaths.bin = [
    inputs.nixpkgs.python39
    inputs.nixpkgs.yq
  ];
  template = ./template.sh;
  name = "common-compute-schedule-parse-terraform";
}
