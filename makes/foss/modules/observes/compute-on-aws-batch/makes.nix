{ outputs
, ...
}:
let
  sharedConfiguration = rec {
    definition = "default";
    environment = [ "PRODUCT_API_TOKEN" ];
    memory = 1800 * vcpus;
    queue = "observes_later";
    setup = [ outputs."/secretsForAwsFromEnv/observesProd" ];
    vcpus = 1;
  };
in
{
  computeOnAwsBatch = {
    observesAnnounceKitEtl = sharedConfiguration // {
      attempts = 5;
      attemptDurationSeconds = 14000;
      command = [ "./m" "observes.job.announcekit.etl" ];
    };

    observesBugsnagEtl = sharedConfiguration // {
      attempts = 5;
      attemptDurationSeconds = 14000;
      command = [ "./m" "observes.job.bugsnag-etl" ];
    };

    observesChecklyEtl = sharedConfiguration // {
      attempts = 5;
      attemptDurationSeconds = 3600;
      command = [ "./m" "observes.job.checkly-etl" ];
    };

    observesCodeEtlAmend = sharedConfiguration // {
      attempts = 5;
      attemptDurationSeconds = 18000;
      command = [ "./m" "observes.scheduled.job.code-etl-amend" ];
      environment = [
        "INTEGRATES_API_TOKEN"
        "PRODUCT_API_TOKEN"
        "SERVICES_API_TOKEN"
      ];
    };

    observesGitlabEtlChallenges = sharedConfiguration // {
      attempts = 5;
      attemptDurationSeconds = 7200;
      command = [ "./m" "observes.job.gitlab-etl.challenges" ];
      environment = [
        "AUTONOMIC_API_TOKEN"
        "PRODUCT_API_TOKEN"
      ];
    };

    observesDelightedEtl = sharedConfiguration // {
      attempts = 5;
      attemptDurationSeconds = 3600;
      command = [ "./m" "observes.job.delighted-etl" ];
    };

    observesDynamoDbForcesEtl = sharedConfiguration // rec {
      attempts = 5;
      attemptDurationSeconds = 18000;
      command = [ "./m" "observes.job.dynamodb-forces-etl" ];
      memory = 1800 * vcpus;
      vcpus = 2;
    };

    observesFormstackEtl = sharedConfiguration // rec {
      attempts = 5;
      attemptDurationSeconds = 14000;
      command = [ "./m" "observes.scheduled.job.formstack-etl" ];
      memory = 1800 * vcpus;
      vcpus = 2;
    };

    observesGitlabEtlDefault = sharedConfiguration // {
      attempts = 5;
      attemptDurationSeconds = 7200;
      command = [ "./m" "observes.job.gitlab-etl.default" ];
      environment = [
        "AUTONOMIC_API_TOKEN"
        "PRODUCT_API_TOKEN"
      ];
    };

    observesGitlabEtlProduct = sharedConfiguration // {
      attempts = 5;
      attemptDurationSeconds = 7200;
      command = [ "./m" "observes.job.gitlab-etl.product" ];
    };

    observesGitlabEtlServices = sharedConfiguration // {
      attempts = 5;
      attemptDurationSeconds = 7200;
      command = [ "./m" "observes.job.gitlab-etl.services" ];
      environment = [
        "PRODUCT_API_TOKEN"
        "SERVICES_API_TOKEN"
      ];
    };

    observesCodeEtlMirror = sharedConfiguration // {
      attempts = 5;
      attemptDurationSeconds = 7200;
      command = [ "./m" "observes.scheduled.job.code-etl-mirror" ];
      environment = [
        "INTEGRATES_API_TOKEN"
        "PRODUCT_API_TOKEN"
        "SERVICES_API_TOKEN"
      ];
      queue = "observes_soon";
    };

    observesCodeEtlUpload = sharedConfiguration // {
      attempts = 5;
      attemptDurationSeconds = 7200;
      command = [ "./m" "observes.scheduled.job.code-etl-upload" ];
      environment = [
        "INTEGRATES_API_TOKEN"
        "PRODUCT_API_TOKEN"
        "SERVICES_API_TOKEN"
      ];
    };
  };
}
