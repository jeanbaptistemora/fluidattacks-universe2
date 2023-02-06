{outputs}: let
  bins = {
    announceKitEtl = outputs."/computeOnAwsBatch/observesAnnounceKitEtl";
    bugsnagEtl = outputs."/computeOnAwsBatch/observesBugsnagEtl";
    codeEtlMirror = outputs."/observes/etl/code/mirror/all-on-aws";
    codeEtlUpload = outputs."/observes/etl/code/upload/all-on-aws";
    checklyEtl = outputs."/computeOnAwsBatch/observesChecklyEtl";
    delightedEtl = outputs."/computeOnAwsBatch/observesDelightedEtl";
    dynamoDbEtls = outputs."/observes/etl/dynamo/conf";
    formstackEtl = outputs."/computeOnAwsBatch/observesFormstackEtl";
    gitlabEtlProduct = outputs."/computeOnAwsBatch/observesGitlabEtlProduct";
    mailchimpEtl = outputs."/computeOnAwsBatch/observesMailchimpEtl";
    mandrillEtl = outputs."/computeOnAwsBatch/observesMandrillEtl";
  };
  export = builtins.attrValues (
    builtins.mapAttrs (name: output: [name output "/bin/${output.name}"]) bins
  );
in
  export
