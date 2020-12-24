pkgs:

{
  attempts,
  command,
  environment,
  jobname,
  jobqueue,
  name,
  product,
  timeout,
  vcpus,
}:

let
  makeEntrypoint = import ../../../../makes/utils/make-entrypoint pkgs;

  # Granting less than 3600 MB of memory per vCPU is paying for unused resources
  # so let's be greedy and grant it all
  #
  # vCPUs are what control the cost at the end of the day
  memory = vcpus * 3600;
in
  makeEntrypoint {
    arguments = rec {
      envAttempts = attempts;
      envCommand = builtins.toJSON command;
      envJobname = jobname;
      envJobqueue = jobqueue;
      envMemory = memory;
      envName = name;
      envManifest = builtins.toJSON {
        command = command;
        environment = builtins.map (name: {
          name = name;
          value = "\${${name}}";
        }) environment;
        memory = envMemory;
        vcpus = vcpus;
      };
      envProduct = product;
      envShell = "${pkgs.bash}/bin/bash";
      envTimeout = timeout;
      envUtilsBashLibAws = import ../../../../makes/utils/bash-lib/aws pkgs;
      envVcpus =
        if (vcpus <= 4)
        then vcpus
        else abort "Too much vCPUs";
    };
    location = "/bin/${name}";
    name = name;
    template = ../../../../makes/utils/bash-lib/compute-on-aws/entrypoint.sh;
  }
