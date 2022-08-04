# https://github.com/fluidattacks/makes
{outputs, ...}: {
  deployTerraform = {
    modules = {
      commonStatus = {
        setup = [
          outputs."/secretsForEnvFromSops/commonStatusProd"
          outputs."/secretsForTerraformFromEnv/commonStatus"
        ];
        src = "/common/status/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      commonStatus = {
        setup = [
          outputs."/secretsForEnvFromSops/commonStatusDev"
          outputs."/secretsForTerraformFromEnv/commonStatus"
        ];
        src = "/common/status/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    commonStatusProd = {
      vars = [
        "ACCOUNT_ID"
        "ALERT_SMS"
        "ALERT_USERS"
        "API_KEY"
        "ENV_BITBUCKET_PWD"
        "ENV_BITBUCKET_USER"
        "ENV_INTEGRATES_API_TOKEN"
      ];
      manifest = "/common/status/secrets.yaml";
    };
    commonStatusDev = {
      vars = [
        "ACCOUNT_ID"
        "ALERT_SMS"
        "ALERT_USERS"
        "API_KEY"
        "ENV_BITBUCKET_PWD"
        "ENV_BITBUCKET_USER"
        "ENV_INTEGRATES_API_TOKEN"
      ];
      manifest = "/common/status/secrets.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    commonStatus = {
      accountId = "ACCOUNT_ID";
      alertSms = "ALERT_SMS";
      alertUsers = "ALERT_USERS";
      apiKey = "API_KEY";
      envBitBucketPwd = "ENV_BITBUCKET_PWD";
      envBitBucketUser = "ENV_BITBUCKET_USER";
      envIntegratesApiToken = "ENV_INTEGRATES_API_TOKEN";
    };
  };
  testTerraform = {
    modules = {
      commonStatus = {
        setup = [
          outputs."/secretsForEnvFromSops/commonStatusDev"
          outputs."/secretsForTerraformFromEnv/commonStatus"
        ];
        src = "/common/status/infra";
        version = "1.0";
      };
    };
  };
}
