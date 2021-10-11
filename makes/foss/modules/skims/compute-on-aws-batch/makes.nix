{ outputs
, ...
}:
{
  computeOnAwsBatch = {
    skimsOwaspBenchmarkAndUpload = rec {
      attempts = 1;
      attemptDurationSeconds = 86400;
      command = [ "m" "f" "/skims/owasp-benchmark-and-upload" ];
      definition = "makes";
      environment = [ "PRODUCT_API_TOKEN" ];
      memory = vcpus * 1800;
      queue = "dedicated_later";
      setup = [ outputs."/secretsForAwsFromEnv/skimsProd" ];
      vcpus = 4;
    };
    skimsProcessGroup = rec {
      attempts = 1;
      attemptDurationSeconds = 86400;
      command = [ "m" "f" "/skims/process-group" ];
      definition = "makes";
      environment = [ "PRODUCT_API_TOKEN" ];
      memory = vcpus * 1800;
      queue = null;
      setup = [ outputs."/secretsForAwsFromEnv/__default__" ];
      vcpus = 1;
    };
  };
}
