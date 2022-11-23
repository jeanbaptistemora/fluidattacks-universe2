{outputs}: let
  bins = {
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
    mandrillEtl = outputs."/computeOnAwsBatch/observesMandrillEtl";
  };
  export = builtins.attrValues (
    builtins.mapAttrs (name: output: [name output "/bin/${output.name}"]) bins
  );
in
  export
