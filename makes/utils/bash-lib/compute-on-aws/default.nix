pkgs:

{
  attempts,
  command,
  jobname,
  jobqueue,
  name,
  product,
  secrets,
  timeout,
  vcpus,
}:

let
  getSecretFromRuntimeEnv = name: {
    name = name;
    value = "\${${name}}";
  };

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
      envAws = "${pkgs.awscli}/bin/aws";
      envCommand = builtins.toJSON command;
      envEnvsubst = "${pkgs.envsubst}/bin/envsubst";
      envJobname = jobname;
      envJobqueue = jobqueue;
      envJq = "${pkgs.jq}/bin/jq";
      envMemory = memory;
      envName = name;
      envManifestFile = builtins.toFile "manifest" (builtins.toJSON {
        command = command;
        environment = (builtins.map getSecretFromRuntimeEnv secrets) ++ [
          {
            name = "CI";
            value = "true";
          }
          {
            name = "CI_COMMIT_REF_NAME";
            value = "master";
          }
        ];
        memory = envMemory;
        vcpus = vcpus;
      });
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
