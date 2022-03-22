{
  fetchNixpkgs,
  inputs,
  makeTemplate,
  outputs,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.service.scheduler.root;
  pkg = import "${root}/main.nix" fetchNixpkgs projectPath inputs.observesIndex;
  env = pkg.env.dev;
in
  makeTemplate {
    name = "observes-service-jobs-scheduler-env-runtime";
    searchPaths = {
      bin = [env];
      export = builtins.attrValues (builtins.mapAttrs
        (name: output: [name output "/bin/${output.name}"])
        {
          announceKitEtl = outputs."/computeOnAwsBatch/observesAnnounceKitEtl";
          batchStability = outputs."/observes/job/batch-stability";
          bugsnagEtl = outputs."/computeOnAwsBatch/observesBugsnagEtl";
          codeEtlMirror = outputs."/observes/etl/code/mirror/all-on-aws";
          codeEtlUpload = outputs."/observes/etl/code/upload/all-on-aws";
          checklyEtl = outputs."/computeOnAwsBatch/observesChecklyEtl";
          delightedEtl = outputs."/computeOnAwsBatch/observesDelightedEtl";
          dynamoDbEtls = outputs."/observes/etl/dynamo/conf";
          formstackEtl = outputs."/computeOnAwsBatch/observesFormstackEtl";
          gitlabEtlChallenges = outputs."/computeOnAwsBatch/observesGitlabEtlChallenges";
          gitlabEtlDefault = outputs."/computeOnAwsBatch/observesGitlabEtlDefault";
          gitlabEtlProduct = outputs."/computeOnAwsBatch/observesGitlabEtlProduct";
          gitlabEtlServices = outputs."/computeOnAwsBatch/observesGitlabEtlServices";
          mailchimpEtl = outputs."/computeOnAwsBatch/observesMailchimpEtl";
        });
    };
  }
