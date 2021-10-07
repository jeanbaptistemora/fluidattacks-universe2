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
      environment = [ "CI_COMMIT_REF_NAME" "CI_COMMIT_SHA" "PRODUCT_API_TOKEN" ];
      memory = 1800 * vcpus;
      queue = "dedicated_later";
      setup = [ outputs."/secretsForAwsFromEnv/integratesProd" ];
      vcpus = 4;
    };
    integratesSubscriptionsUserToEntity = rec {
      allowDuplicates = false;
      attempts = 2;
      attemptDurationSeconds = 3600;
      command = [ "m" "f" "/integrates/subscriptions/user-to-entity" ];
      definition = "makes";
      includePositionalArgsInName = true;
      environment = [ "CI_COMMIT_REF_NAME" "CI_COMMIT_SHA" "PRODUCT_API_TOKEN" ];
      memory = 1800 * vcpus;
      queue = "dedicated_soon";
      setup = [ outputs."/secretsForAwsFromEnv/integratesProd" ];
      vcpus = 4;
    };
  };
}
