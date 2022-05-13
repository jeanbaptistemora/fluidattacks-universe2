{inputs, ...}: let
  lib = inputs.nixpkgs.lib;
  schedules = import ./schedules.nix;
  mapToBatch = name: value:
    lib.nameValuePair
    "schedule_${name}"
    {
      allowDuplicates = true;
      attempts = value.attempts;
      attemptDurationSeconds = value.timeout;
      command = value.command;
      definition = "makes";
      environment = value.environment;
      includePositionalArgsInName = false;
      memory = value.memory;
      parallel = value.parallel;
      queue = value.queue;
      vcpus = value.cpu;
    };
in {
  imports = [
    ./parse-terraform/makes.nix
  ];
  computeOnAwsBatch = lib.mapAttrs' mapToBatch schedules;
}
