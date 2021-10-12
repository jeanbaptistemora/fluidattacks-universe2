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
  };
}
