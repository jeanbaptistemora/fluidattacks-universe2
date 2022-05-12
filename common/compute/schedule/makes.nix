{inputs, ...}: let
  lib = inputs.nixpkgs.lib;
  schedules = import ./schedules.nix;
  mapToBatch = definition: value:
    lib.nameValuePair
    "schedule_${definition}"
    {
      inherit definition;
      allowDuplicates = true;
      attempts = value.attempts;
      attemptDurationSeconds = value.timeout;
      command = value.command;
      includePositionalArgsInName = false;
      environment = value.environment;
      memory = value.memory;
      queue = value.queue;
      vcpus = value.cpu;
    };
in {
  imports = [
    ./parse-terraform/makes.nix
  ];
  computeOnAwsBatch = lib.mapAttrs' mapToBatch schedules;
}
