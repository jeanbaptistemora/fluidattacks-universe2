# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  fromYaml,
  projectPath,
  outputs,
  ...
}: let
  sizes_conf = fromYaml (
    builtins.readFile (
      projectPath "/common/compute/arch/sizes/data.yaml"
    )
  );
  compute_resources = size: {
    vcpus = sizes_conf."${size}".cpu;
    memory = sizes_conf."${size}".memory;
    queue = sizes_conf."${size}".queue;
  };
  scheduled_job = {
    attempts,
    timeout,
    size,
    command,
  }:
    {
      inherit attempts command;
      attemptDurationSeconds = timeout;
      definition = "prod_observes";
      environment = [
        "CACHIX_AUTH_TOKEN"
        "UNIVERSE_API_TOKEN"
      ];
      setup = [outputs."/secretsForAwsFromGitlab/prodObserves"];
    }
    // compute_resources size;
  clone_job = {
    attempts,
    timeout,
    command,
  }:
    scheduled_job {
      inherit attempts timeout command;
      size = "nano";
    }
    // {
      queue = "clone";
    };
in {
  computeOnAwsBatch = {
    observesAnnounceKitEtl = scheduled_job {
      size = "nano";
      attempts = 3;
      timeout = 43200;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/announcekit"];
    };

    observesBugsnagEtl = scheduled_job {
      size = "nano";
      attempts = 3;
      timeout = 43200;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/bugsnag"];
    };

    observesChecklyEtl = scheduled_job {
      size = "nano";
      attempts = 3;
      timeout = 43200;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/checkly"];
    };

    observesDelightedEtl = scheduled_job {
      size = "nano";
      attempts = 3;
      timeout = 43200;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/delighted"];
    };

    observesFormstackEtl = scheduled_job {
      size = "small";
      attempts = 3;
      timeout = 14000;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/formstack"];
    };

    observesGitlabEtlChallenges = scheduled_job {
      size = "small";
      attempts = 1;
      timeout = 7200;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/gitlab/challenges"];
    };

    observesGitlabEtlDefault = scheduled_job {
      size = "small";
      attempts = 1;
      timeout = 7200;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/gitlab/default"];
    };

    observesGitlabEtlProduct = scheduled_job {
      size = "small";
      attempts = 1;
      timeout = 7200;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/gitlab/universe"];
    };

    observesGitlabEtlServices = scheduled_job {
      size = "small";
      attempts = 1;
      timeout = 7200;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/gitlab/services"];
    };

    observesMailchimpEtl = scheduled_job {
      size = "nano";
      attempts = 1;
      timeout = 864000;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/mailchimp"];
    };

    observesMandrillEtl = scheduled_job {
      size = "nano";
      attempts = 1;
      timeout = 7200;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/mandrill"];
    };

    observesCodeEtlMirror = clone_job {
      attempts = 3;
      timeout = 7200;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/code/mirror"];
    };

    observesCodeEtlUpload = scheduled_job {
      size = "nano";
      attempts = 3;
      timeout = 28800;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/code/upload"];
    };

    observesDynamoV2Etl = scheduled_job {
      size = "nano";
      attempts = 3;
      timeout = 7200;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/dynamo/v2"];
    };

    observesDynamoV2EtlBig = scheduled_job {
      size = "medium";
      attempts = 1;
      timeout = 172800;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/dynamo/v2"];
    };

    observesDynamoParallel = scheduled_job {
      size = "large";
      attempts = 1;
      timeout = 259200;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/dynamo/parallel"];
    };

    observesDynamoPrepare = scheduled_job {
      size = "nano";
      attempts = 1;
      timeout = 1800;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/dynamo/prepare"];
    };

    observesDynamoV3EtlBig = scheduled_job {
      size = "medium";
      attempts = 1;
      timeout = 172800;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/dynamo/v3"];
    };
  };
}
