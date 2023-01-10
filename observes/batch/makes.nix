{
  fromYaml,
  projectPath,
  outputs,
  ...
}: let
  composition = let
    reverseList = xs: let l = builtins.length xs; in builtins.genList (n: builtins.elemAt xs (l - n - 1)) l;
    apply = x: f: f x;
  in
    # composition of functions
    functions: val: builtins.foldl' apply val (reverseList functions);
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
    name,
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
      ];
      setup = [outputs."/secretsForAwsFromGitlab/prodObserves"];
      tags = {
        "Name" = name;
        "management:area" = "cost";
        "management:product" = "observes";
        "management:type" = "product";
      };
    }
    // compute_resources size;

  with_universe_token = job: job // {environment = job.environment ++ ["UNIVERSE_API_TOKEN"];};
  parrallel_job = parallel: let
    parallel_conf =
      if parallel >= 2
      then {inherit parallel;}
      else {};
  in
    job: job // parallel_conf;

  clone_job = {
    name,
    attempts,
    timeout,
    command,
  }:
    scheduled_job {
      inherit name attempts timeout command;
      size = "observes_clone";
    }
    // {
      queue = "observes_clone";
    };
in {
  computeOnAwsBatch = {
    observesAnnounceKitEtl = scheduled_job {
      name = "announcekit_etl";
      size = "observes_nano";
      attempts = 3;
      timeout = 12 * 3600;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/announcekit"];
    };

    observesBugsnagEtl = scheduled_job {
      name = "bugsnag_etl";
      size = "observes_nano";
      attempts = 3;
      timeout = 12 * 3600;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/bugsnag"];
    };

    observesChecklyEtl = scheduled_job {
      name = "checkly_etl";
      size = "observes_nano";
      attempts = 3;
      timeout = 12 * 3600;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/checkly"];
    };

    observesDelightedEtl = scheduled_job {
      name = "delighted_etl";
      size = "observes_nano";
      attempts = 3;
      timeout = 12 * 3600;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/delighted"];
    };

    observesFormstackEtl = scheduled_job {
      name = "formstack_etl";
      size = "observes_small";
      attempts = 3;
      timeout = 4 * 3600;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/formstack"];
    };

    observesGitlabEtlChallenges = composition [with_universe_token scheduled_job] {
      name = "gitlab_challenges_etl";
      size = "observes_medium";
      attempts = 1;
      timeout = 1 * 3600;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/gitlab/challenges"];
    };

    observesGitlabEtlDefault = composition [with_universe_token scheduled_job] {
      name = "gitlab_default_etl";
      size = "observes_medium";
      attempts = 1;
      timeout = 1 * 3600;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/gitlab/default"];
    };

    observesGitlabEtlProduct = composition [with_universe_token scheduled_job] {
      name = "gitlab_product_etl";
      size = "observes_medium";
      attempts = 1;
      timeout = 6 * 3600;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/gitlab/universe"];
    };

    observesGitlabEtlServices = composition [with_universe_token scheduled_job] {
      name = "gitlab_services_etl";
      size = "observes_medium";
      attempts = 1;
      timeout = 1 * 3600;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/gitlab/services"];
    };

    observesMailchimpEtl = scheduled_job {
      name = "mailchimp_etl";
      size = "observes_medium";
      attempts = 1;
      timeout = 24 * 3600;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/mailchimp"];
    };

    observesMandrillEtl = scheduled_job {
      name = "mandrill_etl";
      size = "observes_nano";
      attempts = 1;
      timeout = 2 * 3600;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/mandrill"];
    };

    observesCodeEtlMirror = composition [with_universe_token clone_job] {
      name = "code_mirror";
      attempts = 3;
      timeout = 2 * 3600;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/code/mirror"];
    };

    observesCodeEtlUpload = composition [with_universe_token scheduled_job] {
      name = "code_upload";
      size = "observes_nano";
      attempts = 3;
      timeout = 8 * 3600;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/code/upload"];
    };

    observesDynamoSchema = scheduled_job {
      name = "dynamo_etl_determine_schema";
      size = "observes_medium";
      attempts = 3;
      timeout = 48 * 3600;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/dynamo_etl_conf/jobs/determine-schema"];
    };

    observesDynamoV2Etl = scheduled_job {
      name = "dynamo_etl_v2";
      size = "observes_nano";
      attempts = 3;
      timeout = 2 * 3600;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/dynamo/v2"];
    };

    observesDynamoV2EtlBig = scheduled_job {
      name = "dynamo_etl_v2_big";
      size = "observes_medium";
      attempts = 1;
      timeout = 48 * 3600;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/dynamo/v2"];
    };

    observesDynamoParallel = parrallel_job 30 (scheduled_job {
      name = "dynamo_etl_parallel";
      size = "observes_nano";
      attempts = 1;
      timeout = 24 * 3600;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/dynamo/parallel"];
    });

    observesDynamoPrepare = scheduled_job {
      name = "dynamo_etl_prepare";
      size = "observes_nano";
      attempts = 1;
      timeout = 1800;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/dynamo_etl_conf/jobs/prepare"];
    };

    observesDynamoV3EtlBig = scheduled_job {
      name = "dynamo_etl_v3_big";
      size = "observes_medium";
      attempts = 1;
      timeout = 48 * 3600;
      command = ["m" "gitlab:fluidattacks/universe@trunk" "/observes/etl/dynamo/v3"];
    };
  };
}
