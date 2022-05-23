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
      };

    observesGitlabEtlDefault =
      sharedConfiguration
      // {
        attemptDurationSeconds = 7200;
        command = ["m" "f" "/observes/etl/gitlab/default"];
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
        queue = "unlimited_spot";
      };

    observesCodeEtlUpload =
      sharedConfiguration
      // {
        attemptDurationSeconds = 28800;
        command = ["m" "f" "/observes/etl/code/upload"];
        queue = "unlimited_spot";
      };

    observesCodeEtlMigration2 =
      sharedConfiguration
      // {
        queue = "limited_dedicated";
        attempts = 1;
        attemptDurationSeconds = 604800;
        command = ["m" "f" "/observes/etl/code/upload/migration/fa-hash/v2"];
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
        attemptDurationSeconds = 172800;
        attempts = 1;
        command = ["m" "f" "/observes/etl/dynamo/v2"];
        queue = "unlimited_dedicated";
      };

    observesDbMigration =
      sharedConfiguration
      // {
        queue = "limited_dedicated";
        attempts = 1;
        attemptDurationSeconds = 172800;
        command = ["m" "f" "/observes/job/migration"];
      };
  };
}
