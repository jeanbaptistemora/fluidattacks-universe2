# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesStatus = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForEnvFromSops/makesStatusProd"
          outputs."/secretsForTerraformFromEnv/makesStatus"
        ];
        src = "/makes/foss/modules/makes/status/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesStatus = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/makesStatusDev"
          outputs."/secretsForTerraformFromEnv/makesStatus"
        ];
        src = "/makes/foss/modules/makes/status/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    makesStatusProd = {
      vars = [
        "BITBUCKET_PWD"
        "BITBUCKET_USER"
        "CHECKLY_API_KEY"
        "INTEGRATES_API_TOKEN"
        "STATUS_ALERT_CHANNEL_USERS"
      ];
      manifest = "/makes/foss/modules/makes/secrets/prod.yaml";
    };
    makesStatusDev = {
      vars = [
        "BITBUCKET_PWD"
        "BITBUCKET_USER"
        "CHECKLY_API_KEY"
        "INTEGRATES_API_TOKEN"
        "STATUS_ALERT_CHANNEL_USERS"
      ];
      manifest = "/makes/foss/modules/makes/secrets/dev.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    makesStatus = {
      alertChannelUsers = "STATUS_ALERT_CHANNEL_USERS";
      bitbucketPwd = "BITBUCKET_PWD";
      bitbucketUser = "BITBUCKET_USER";
      checklyApiKey = "CHECKLY_API_KEY";
      integratesApiToken = "INTEGRATES_API_TOKEN";
    };
  };
  testTerraform = {
    modules = {
      makesStatus = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/makesStatusDev"
          outputs."/secretsForTerraformFromEnv/makesStatus"
        ];
        src = "/makes/foss/modules/makes/status/infra";
        version = "1.0";
      };
    };
  };
}
