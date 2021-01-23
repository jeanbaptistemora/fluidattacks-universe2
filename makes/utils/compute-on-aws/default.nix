path: pkgs:

{ attempts
, command
, jobname
, jobqueue
, name
, product
, secrets
, timeout
, vcpus
}:
let
  getSecretFromRuntimeEnv = name: {
    inherit name;
    value = "\${${name}}";
  };

  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path pkgs;

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
    envCommandFile = builtins.toFile "command" (builtins.toJSON command);
    envEnvsubst = "${pkgs.envsubst}/bin/envsubst";
    envJobname = jobname;
    envJobqueue = jobqueue;
    envJq = "${pkgs.jq}/bin/jq";
    envManifestFile = builtins.toFile "manifest" (builtins.toJSON {
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
      inherit vcpus;
    });
    envMemory = memory;
    envProduct = product;
    envTimeout = timeout;
    envUtilsBashLibAws = import (path "/makes/utils/aws") path pkgs;
    envVcpus =
      if (vcpus <= 4)
      then vcpus
      else abort "Too much vCPUs";
  };
  location = "/bin/${name}";
  inherit name;
  template = path "/makes/utils/compute-on-aws/entrypoint.sh";
}
