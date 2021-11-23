{ outputs
, ...
}:
let
  sharedConfiguration = rec {
    attempts = 5;
    definition = "makes";
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
      attemptDurationSeconds = 14000;
      command = [ "m" "f" "/observes/etl/announcekit" ];
    };

    observesBugsnagEtl = sharedConfiguration // {
      attemptDurationSeconds = 14000;
      command = [ "m" "f" "/observes/etl/bugsnag" ];
    };

    observesChecklyEtl = sharedConfiguration // {
      attemptDurationSeconds = 3600;
      command = [ "m" "f" "/observes/job/checkly-etl" ];
    };

    observesGitlabEtlChallenges = sharedConfiguration // {
      attemptDurationSeconds = 7200;
      command = [ "m" "f" "/observes/job/gitlab-etl/challenges" ];
      environment = [
        "AUTONOMIC_API_TOKEN"
        "PRODUCT_API_TOKEN"
      ];
    };

    observesDelightedEtl = sharedConfiguration // {
      attemptDurationSeconds = 3600;
      command = [ "m" "f" "/observes/job/delighted-etl" ];
    };

    observesDynamoDbForcesEtl = sharedConfiguration // rec {
      attemptDurationSeconds = 18000;
      command = [ "m" "f" "/observes/job/dynamodb-forces-etl" ];
      memory = 1800 * vcpus;
      vcpus = 2;
    };

    observesFormstackEtl = sharedConfiguration // rec {
      attemptDurationSeconds = 14000;
      command = [ "m" "f" "/observes/scheduled/job/formstack-etl" ];
      memory = 1800 * vcpus;
      vcpus = 2;
    };

    observesGitlabEtlDefault = sharedConfiguration // {
      attemptDurationSeconds = 7200;
      command = [ "m" "f" "/observes/job/gitlab-etl/default" ];
      environment = [
        "AUTONOMIC_API_TOKEN"
        "PRODUCT_API_TOKEN"
      ];
    };

    observesGitlabEtlProduct = sharedConfiguration // {
      attemptDurationSeconds = 7200;
      command = [ "m" "f" "/observes/job/gitlab-etl/product" ];
    };

    observesGitlabEtlServices = sharedConfiguration // {
      attemptDurationSeconds = 7200;
      command = [ "m" "f" "/observes/job/gitlab-etl/services" ];
      environment = [ "PRODUCT_API_TOKEN" "SERVICES_API_TOKEN" ];
    };

    observesCodeEtlMirror = sharedConfiguration // {
      attemptDurationSeconds = 7200;
      command = [ "m" "f" "/observes/job/code-etl/mirror" ];
      environment = [
        "INTEGRATES_API_TOKEN"
        "PRODUCT_API_TOKEN"
        "SERVICES_API_TOKEN"
      ];
      queue = "observes_soon";
    };

    observesCodeEtlUpload = sharedConfiguration // {
      attemptDurationSeconds = 28800;
      command = [ "m" "f" "/observes/job/code-etl/upload" ];
      environment = [
        "INTEGRATES_API_TOKEN"
        "PRODUCT_API_TOKEN"
        "SERVICES_API_TOKEN"
      ];
    };

    observesDynamoDbIntegratesEtl = sharedConfiguration // {
      attemptDurationSeconds = 7200;
      command = [ "m" "f" "/observes/job/dynamodb-table-etl" ];
      queue = "observes_soon";
    };
  };
}
