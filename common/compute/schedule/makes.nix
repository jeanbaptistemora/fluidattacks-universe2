{
  fromYaml,
  inputs,
  projectPath,
  ...
}: let
  lib = inputs.nixpkgs.lib;
  schedules = fromYaml (
    builtins.readFile ./data.yaml
  );
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
      tags = value.tags;
      includePositionalArgsInName = false;
      memory = sizes.${value.size}.memory;
      parallel = value.parallel;
      queue = sizes.${value.size}.queue;
      vcpus = sizes.${value.size}.cpu;
    };
in {
  computeOnAwsBatch = lib.mapAttrs' mapToBatch schedules;
  imports = [
    ./parse-terraform/makes.nix
    ./test/makes.nix
  ];
}
