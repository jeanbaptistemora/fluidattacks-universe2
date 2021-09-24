{ outputs
, ...
}:
{
  computeOnAwsBatch = {
    skimsOwaspBenchmarkAndUpload = {
      allowDuplicates = false;
      attempts = 1;
      attemptDurationSeconds = 86400;
      command = [ "m" "/skims/owasp-benchmark-and-upload" ];
      definition = "makes";
      environment = [ "PRODUCT_API_TOKEN" ];
      memory = 4 * 1800;
      name = "skims-benchmark";
      queue = "dedicated_later";
      setup = [ outputs."/secretsForAwsFromEnv/skimsProd" ];
      vcpus = 4;
    };
  };
}
