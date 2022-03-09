# https://github.com/fluidattacks/makes
{outputs, ...}: {
  deployTerraform = {
    modules = {
      makesStatus = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodMakes"
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
        "CHECKLY_ACCOUNT_ID"
        "CHECKLY_API_KEY"
        "INTEGRATES_API_TOKEN"
        "STATUS_ALERT_CHANNEL_USERS"
      ];
      manifest = "/makes/secrets/prod.yaml";
    };
    makesStatusDev = {
      vars = [
        "BITBUCKET_PWD"
        "BITBUCKET_USER"
        "CHECKLY_ACCOUNT_ID"
        "CHECKLY_API_KEY"
        "INTEGRATES_API_TOKEN"
        "STATUS_ALERT_CHANNEL_USERS"
      ];
      manifest = "/makes/secrets/dev.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    makesStatus = {
      alertChannelUsers = "STATUS_ALERT_CHANNEL_USERS";
      bitbucketPwd = "BITBUCKET_PWD";
      bitbucketUser = "BITBUCKET_USER";
      checklyAccountId = "CHECKLY_ACCOUNT_ID";
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
