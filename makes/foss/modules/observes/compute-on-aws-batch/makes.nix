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
      command = [ "m" "f" "/observes/etl/checkly" ];
    };

    observesGitlabEtlChallenges = sharedConfiguration // {
      attemptDurationSeconds = 7200;
      command = [ "m" "f" "/observes/etl/gitlab/challenges" ];
      environment = [
        "AUTONOMIC_API_TOKEN"
        "PRODUCT_API_TOKEN"
      ];
    };

    observesDelightedEtl = sharedConfiguration // {
      attemptDurationSeconds = 3600;
      command = [ "m" "f" "/observes/etl/delighted" ];
    };

    observesDynamoDbForcesEtl = sharedConfiguration // rec {
      attemptDurationSeconds = 18000;
      command = [ "m" "f" "/observes/etl/dynamo/forces" ];
      memory = 1800 * vcpus;
      vcpus = 2;
    };

    observesFormstackEtl = sharedConfiguration // rec {
      attemptDurationSeconds = 14000;
      command = [ "m" "f" "/observes/etl/formstack" ];
      memory = 1800 * vcpus;
      vcpus = 2;
    };

    observesGitlabEtlDefault = sharedConfiguration // {
      attemptDurationSeconds = 7200;
      command = [ "m" "f" "/observes/etl/gitlab/default" ];
      environment = [
        "AUTONOMIC_API_TOKEN"
        "PRODUCT_API_TOKEN"
      ];
    };

    observesGitlabEtlProduct = sharedConfiguration // {
      attemptDurationSeconds = 7200;
      command = [ "m" "f" "/observes/etl/gitlab/product" ];
    };

    observesGitlabEtlServices = sharedConfiguration // {
      attemptDurationSeconds = 7200;
      command = [ "m" "f" "/observes/etl/gitlab/services" ];
      environment = [ "PRODUCT_API_TOKEN" "SERVICES_API_TOKEN" ];
    };

    observesCodeEtlMirror = sharedConfiguration // {
      attemptDurationSeconds = 7200;
      command = [ "m" "f" "/observes/etl/code/mirror" ];
      environment = [
        "INTEGRATES_API_TOKEN"
        "PRODUCT_API_TOKEN"
        "SERVICES_API_TOKEN"
      ];
      queue = "observes_soon";
    };

    observesCodeEtlUpload = sharedConfiguration // {
      attemptDurationSeconds = 28800;
      command = [ "m" "f" "/observes/etl/code/upload" ];
      environment = [
        "INTEGRATES_API_TOKEN"
        "PRODUCT_API_TOKEN"
        "SERVICES_API_TOKEN"
      ];
    };

    observesDynamoTableEtl = sharedConfiguration // {
      attemptDurationSeconds = 7200;
      command = [ "m" "f" "/observes/etl/dynamo/table" ];
      queue = "observes_soon";
    };

    observesDynamoTableEtlBig = sharedConfiguration // {
      attemptDurationSeconds = 18000;
      command = [ "m" "f" "/observes/etl/dynamo/table" ];
      queue = "observes_soon";
    };
  };
}
