# https://github.com/fluidattacks/makes
{outputs, ...}: {
  deployTerraform = {
    modules = {
      commonStatus = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodMakes"
          outputs."/secretsForEnvFromSops/commonStatusProd"
          outputs."/secretsForTerraformFromEnv/commonStatus"
        ];
        src = "/makes/foss/modules/common/status/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      commonStatus = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/commonStatusDev"
          outputs."/secretsForTerraformFromEnv/commonStatus"
        ];
        src = "/makes/foss/modules/common/status/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    commonStatusProd = {
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
    commonStatusDev = {
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
    commonStatus = {
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
      commonStatus = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/commonStatusDev"
          outputs."/secretsForTerraformFromEnv/commonStatus"
        ];
        src = "/makes/foss/modules/common/status/infra";
        version = "1.0";
      };
    };
  };
}
