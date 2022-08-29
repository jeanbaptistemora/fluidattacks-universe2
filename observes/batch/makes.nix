let
  sharedConfiguration = rec {
    attempts = 5;
    definition = "prod_observes";
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    memory = 1800 * vcpus;
    queue = "small";
    vcpus = 1;
  };
in {
  computeOnAwsBatch = {
    observesAnnounceKitEtl =
      sharedConfiguration
      // {
        attemptDurationSeconds = 43200;
        command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/announcekit"];
      };

    observesBugsnagEtl =
      sharedConfiguration
      // {
        attemptDurationSeconds = 43200;
        command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/bugsnag"];
      };

    observesChecklyEtl =
      sharedConfiguration
      // {
        attemptDurationSeconds = 43200;
        command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/checkly"];
      };

    observesDelightedEtl =
      sharedConfiguration
      // {
        attemptDurationSeconds = 43200;
        command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/delighted"];
      };

    observesFormstackEtl =
      sharedConfiguration
      // rec {
        attemptDurationSeconds = 14000;
        command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/formstack"];
        memory = 1800 * vcpus;
        vcpus = 2;
      };

    observesGitlabEtlChallenges =
      sharedConfiguration
      // {
        attemptDurationSeconds = 7200;
        command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/gitlab/challenges"];
      };

    observesGitlabEtlDefault =
      sharedConfiguration
      // {
        attemptDurationSeconds = 7200;
        command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/gitlab/default"];
      };

    observesGitlabEtlProduct =
      sharedConfiguration
      // {
        attemptDurationSeconds = 7200;
        command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/gitlab/universe"];
      };

    observesGitlabEtlServices =
      sharedConfiguration
      // {
        attemptDurationSeconds = 7200;
        command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/gitlab/services"];
      };

    observesMailchimpEtl =
      sharedConfiguration
      // {
        attempts = 1;
        attemptDurationSeconds = 864000;
        command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/mailchimp"];
      };

    observesMandrillEtl =
      sharedConfiguration
      // {
        attempts = 1;
        attemptDurationSeconds = 7200;
        command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/mandrill"];
      };

    observesCodeEtlMirror =
      sharedConfiguration
      // {
        queue = "clone";
        attemptDurationSeconds = 7200;
        command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/code/mirror"];
      };

    observesCodeEtlUpload =
      sharedConfiguration
      // {
        attemptDurationSeconds = 28800;
        command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/code/upload"];
      };

    observesCodeEtlMigration2 =
      sharedConfiguration
      // {
        attempts = 1;
        attemptDurationSeconds = 604800;
        command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/code/upload/migration/fa-hash/v2"];
      };

    observesDynamoV2Etl =
      sharedConfiguration
      // {
        attemptDurationSeconds = 7200;
        command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/dynamo/v2"];
      };

    observesDynamoV2EtlBig =
      sharedConfiguration
      // {
        attemptDurationSeconds = 172800;
        attempts = 1;
        command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/dynamo/v2"];
        vcpus = 4;
        memory = 7600;
        queue = "medium";
      };

    observesDynamoParallel =
      sharedConfiguration
      // {
        attemptDurationSeconds = 259200;
        attempts = 1;
        command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/dynamo/parallel"];
        queue = "large";
        vcpus = 8;
        memory = 15200;
        parallel = 10;
      };

    observesDynamoPrepare =
      sharedConfiguration
      // {
        attemptDurationSeconds = 1800;
        attempts = 1;
        command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/dynamo/prepare"];
      };

    observesDynamoV3EtlBig =
      sharedConfiguration
      // {
        attemptDurationSeconds = 172800;
        attempts = 1;
        command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/dynamo/v3"];
        vcpus = 4;
        memory = 7600;
        queue = "medium";
      };

    observesDbMigration =
      sharedConfiguration
      // {
        attempts = 1;
        attemptDurationSeconds = 172800;
        command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/job/migration"];
      };
  };
}
