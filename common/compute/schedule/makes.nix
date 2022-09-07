# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  fromYaml,
  projectPath,
  inputs,
  ...
}: let
  lib = inputs.nixpkgs.lib;
  schedules = import ./schedules.nix;
  sizes = fromYaml (
    builtins.readFile (
      projectPath "/common/compute/arch/sizes/data.yaml"
    )
  );
  mapToBatch = name: value:
    lib.nameValuePair
    "schedule_${name}"
    {
      allowDuplicates = true;
      attempts = value.attempts;
      attemptDurationSeconds = value.timeout;
      command = value.command;
      definition = value.awsRole;
      environment = value.environment;
      includePositionalArgsInName = false;
      memory = sizes.${value.size}.memory;
      parallel = value.parallel;
      queue = sizes.${value.size}.queue;
      vcpus = sizes.${value.size}.cpu;
    };
in {
  imports = [
    ./parse-terraform/makes.nix
  ];
  computeOnAwsBatch = lib.mapAttrs' mapToBatch schedules;
}
