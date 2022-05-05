{outputs, ...}: {
  computeOnAwsBatch = {
    skimsOwaspBenchmarkAndUpload = rec {
      attempts = 1;
      attemptDurationSeconds = 86400;
      command = ["m" "f" "/skims/owasp-benchmark-and-upload"];
      definition = "makes";
      environment = ["PRODUCT_API_TOKEN"];
      memory = vcpus * 1800;
      queue = "limited_dedicated";
      setup = [outputs."/secretsForAwsFromEnv/prodSkims"];
      vcpus = 4;
    };
  };
}
