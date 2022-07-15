{outputs, ...}: let
  sharedConfiguration = rec {
    attempts = 5;
    definition = "makes";
    environment = ["UNIVERSE_API_TOKEN"];
    memory = 1800 * vcpus;
    queue = "small";
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
        command = ["m" "f" "/observes/etl/gitlab/universe"];
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
      };

    observesCodeEtlMirror =
      sharedConfiguration
      // {
        queue = "clone";
        attemptDurationSeconds = 7200;
        command = ["m" "f" "/observes/etl/code/mirror"];
      };

    observesCodeEtlUpload =
      sharedConfiguration
      // {
        attemptDurationSeconds = 28800;
        command = ["m" "f" "/observes/etl/code/upload"];
      };

    observesCodeEtlMigration2 =
      sharedConfiguration
      // {
        attempts = 1;
        attemptDurationSeconds = 604800;
        command = ["m" "f" "/observes/etl/code/upload/migration/fa-hash/v2"];
      };

    observesDynamoV2Etl =
      sharedConfiguration
      // {
        attemptDurationSeconds = 7200;
        command = ["m" "f" "/observes/etl/dynamo/v2"];
      };

    observesDynamoV2EtlBig =
      sharedConfiguration
      // {
        attemptDurationSeconds = 172800;
        attempts = 1;
        command = ["m" "f" "/observes/etl/dynamo/v2"];
        vcpus = 4;
        memory = 7600;
        queue = "medium";
      };

    observesDynamoParallel =
      sharedConfiguration
      // {
        attemptDurationSeconds = 36000;
        attempts = 1;
        command = ["m" "f" "/observes/etl/dynamo/parallel"];
        parallel = 100;
      };

    observesDynamoPrepare =
      sharedConfiguration
      // {
        attemptDurationSeconds = 1800;
        attempts = 1;
        command = ["m" "f" "/observes/etl/dynamo/prepare"];
      };

    observesDynamoV3EtlBig =
      sharedConfiguration
      // {
        attemptDurationSeconds = 172800;
        attempts = 1;
        command = ["m" "f" "/observes/etl/dynamo/v3"];
        vcpus = 4;
        memory = 7600;
        queue = "medium";
      };

    observesDbMigration =
      sharedConfiguration
      // {
        attempts = 1;
        attemptDurationSeconds = 172800;
        command = ["m" "f" "/observes/job/migration"];
      };
  };
}
