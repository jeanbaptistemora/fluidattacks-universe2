{ outputs
, ...
}:
let
  sharedConfiguration = rec {
    definition = "default";
    environment = [ "PRODUCT_API_TOKEN" ];
    memory = 1800 * vcpus;
    setup = [ outputs."/secretsForAwsFromEnv/observesProd" ];
    vcpus = 1;
  };
in
{
  computeOnAwsBatch = {
    observesBugsnagEtl = sharedConfiguration // {
      attempts = 5;
      attemptDurationSeconds = 14000;
      command = [ "./m" "observes.job.bugsnag-etl" ];
      queue = "observes_later";
    };

    observesChecklyEtl = sharedConfiguration // {
      attempts = 5;
      attemptDurationSeconds = 3600;
      command = [ "./m" "observes.job.checkly-etl" ];
      queue = "observes_later";
    };

    observesCodeEtlAmend = sharedConfiguration // {
      attempts = 5;
      attemptDurationSeconds = 18000;
      command = [ "./m" "observes.scheduled.job.code-etl-amend" ];
      queue = "observes_later";
      environment = [
        "INTEGRATES_API_TOKEN"
        "PRODUCT_API_TOKEN"
        "SERVICES_API_TOKEN"
      ];
    };

    observesDelightedEtl = sharedConfiguration // {
      attempts = 5;
      attemptDurationSeconds = 3600;
      command = [ "./m" "observes.job.delighted-etl" ];
      queue = "observes_later";
    };

    observesDynamoDbForcesEtl = sharedConfiguration // rec {
      attempts = 5;
      attemptDurationSeconds = 18000;
      command = [ "./m" "observes.job.dynamodb-forces-etl" ];
      queue = "observes_later";
      memory = 1800 * vcpus;
      vcpus = 2;
    };
  };
}
