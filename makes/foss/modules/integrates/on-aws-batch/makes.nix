{ outputs
, ...
}:
{
  computeOnAwsBatch = {
    integratesScheduler = rec {
      allowDuplicates = false;
      attempts = 1;
      attemptDurationSeconds = 43200;
      command = [ "m" "f" "/integrates/scheduler" ];
      definition = "makes";
      includePositionalArgsInName = true;
      environment = [ "PRODUCT_API_TOKEN" ];
      memory = 1800 * vcpus;
      queue = "dedicated_later";
      setup = [ outputs."/secretsForAwsFromEnv/prodIntegrates" ];
      vcpus = 4;
    };
    integratesSubscriptionsDailyDigest = rec {
      allowDuplicates = false;
      attempts = 2;
      attemptDurationSeconds = 3600;
      command = [ "m" "f" "/integrates/subscriptions/daily-digest" ];
      definition = "makes";
      includePositionalArgsInName = true;
      environment = [ "PRODUCT_API_TOKEN" ];
      memory = 1800 * vcpus;
      queue = "dedicated_soon";
      setup = [ outputs."/secretsForAwsFromEnv/prodIntegrates" ];
      vcpus = 4;
    };
  };
}
