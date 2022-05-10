{outputs, ...}: let
  sharedConfiguration = rec {
    attempts = 5;
    definition = "makes";
    environment = ["PRODUCT_API_TOKEN"];
    memory = 1800 * vcpus;
    queue = "limited_spot";
    setup = [outputs."/secretsForAwsFromEnv/prodObserves"];
    vcpus = 1;
  };
in {
  computeOnAwsBatch = {
    observesAnnounceKitEtl =
      sharedConfiguration
      // {
        attemptDurationSeconds = 43200;
        command = ["m" "f" "/observes/etl/announcekit"];
      };

    observesBugsnagEtl =
      sharedConfiguration
      // {
        attemptDurationSeconds = 43200;
        command = ["m" "f" "/observes/etl/bugsnag"];
      };

    observesChecklyEtl =
      sharedConfiguration
      // {
        attemptDurationSeconds = 43200;
        command = ["m" "f" "/observes/etl/checkly"];
      };

    observesDelightedEtl =
      sharedConfiguration
      // {
        attemptDurationSeconds = 43200;
        command = ["m" "f" "/observes/etl/delighted"];
      };

    observesFormstackEtl =
      sharedConfiguration
      // rec {
        attemptDurationSeconds = 14000;
        command = ["m" "f" "/observes/etl/formstack"];
        memory = 1800 * vcpus;
        vcpus = 2;
      };

    observesGitlabEtlChallenges =
      sharedConfiguration
      // {
        attemptDurationSeconds = 7200;
        command = ["m" "f" "/observes/etl/gitlab/challenges"];
        environment = [
          "AUTONOMIC_API_TOKEN"
          "PRODUCT_API_TOKEN"
        ];
      };

    observesGitlabEtlDefault =
      sharedConfiguration
      // {
        attemptDurationSeconds = 7200;
        command = ["m" "f" "/observes/etl/gitlab/default"];
        environment = [
          "AUTONOMIC_API_TOKEN"
          "PRODUCT_API_TOKEN"
        ];
      };

    observesGitlabEtlProduct =
      sharedConfiguration
      // {
        attemptDurationSeconds = 7200;
        command = ["m" "f" "/observes/etl/gitlab/product"];
      };

    observesGitlabEtlServices =
      sharedConfiguration
      // {
        attemptDurationSeconds = 7200;
        command = ["m" "f" "/observes/etl/gitlab/services"];
        environment = ["PRODUCT_API_TOKEN" "SERVICES_API_TOKEN"];
      };

    observesMailchimpEtl =
      sharedConfiguration
      // {
        attempts = 1;
        attemptDurationSeconds = 864000;
        command = ["m" "f" "/observes/etl/mailchimp"];
        queue = "unlimited_spot";
      };

    observesCodeEtlMirror =
      sharedConfiguration
      // {
        attemptDurationSeconds = 7200;
        command = ["m" "f" "/observes/etl/code/mirror"];
        environment = [
          "INTEGRATES_API_TOKEN"
          "PRODUCT_API_TOKEN"
          "SERVICES_API_TOKEN"
        ];
        queue = "unlimited_spot";
      };

    observesCodeEtlUpload =
      sharedConfiguration
      // {
        attemptDurationSeconds = 28800;
        command = ["m" "f" "/observes/etl/code/upload"];
        environment = [
          "INTEGRATES_API_TOKEN"
          "PRODUCT_API_TOKEN"
          "SERVICES_API_TOKEN"
        ];
        queue = "unlimited_spot";
      };

    observesCodeEtlMigration2 =
      sharedConfiguration
      // {
        queue = "limited_dedicated";
        attempts = 1;
        attemptDurationSeconds = 604800;
        command = ["m" "f" "/observes/etl/code/upload/migration/fa-hash/v2"];
        environment = [
          "PRODUCT_API_TOKEN"
          "SERVICES_API_TOKEN"
        ];
      };

    observesDynamoV2Etl =
      sharedConfiguration
      // {
        attemptDurationSeconds = 7200;
        command = ["m" "f" "/observes/etl/dynamo/v2"];
        queue = "unlimited_spot";
      };

    observesDynamoV2EtlBig =
      sharedConfiguration
      // {
        attemptDurationSeconds = 86400;
        command = ["m" "f" "/observes/etl/dynamo/v2"];
        queue = "unlimited_spot";
      };

    observesDbMigration =
      sharedConfiguration
      // {
        queue = "limited_dedicated";
        attempts = 1;
        attemptDurationSeconds = 172800;
        command = ["m" "f" "/observes/job/migration"];
        environment = [
          "PRODUCT_API_TOKEN"
        ];
      };
  };
}
