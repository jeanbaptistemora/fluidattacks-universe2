{ outputs
, ...
}:
{
  computeOnAwsBatch = {
    integratesMigration = rec {
      allowDuplicates = false;
      attempts = 1;
      attemptDurationSeconds = 64800;
      command = [ "m" "f" "/integrates/db/migration" ];
      definition = "makes";
      includePositionalArgsInName = true;
      environment = [ "PRODUCT_API_TOKEN" ];
      memory = 1800 * vcpus;
      queue = "dedicated_soon";
      setup = [ outputs."/secretsForAwsFromEnv/prodIntegrates" ];
      vcpus = 4;
    };
    integratesScheduler = rec {
      allowDuplicates = false;
      attempts = 1;
      attemptDurationSeconds = 86400;
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
