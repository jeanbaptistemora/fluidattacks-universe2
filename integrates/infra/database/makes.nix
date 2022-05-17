{outputs, ...}: {
  deployTerraform = {
    modules = {
      integratesDatabase = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodIntegrates"
          outputs."/secretsForEnvFromSops/integratesDatabaseProd"
          outputs."/secretsForTerraformFromEnv/integratesDatabase"
        ];
        src = "/integrates/infra/database/src";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      integratesDatabase = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/integratesDatabaseDev"
          outputs."/secretsForTerraformFromEnv/integratesDatabase"
        ];
        src = "/integrates/infra/database/src";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    integratesDatabaseDev = {
      vars = [
        "CLOUDFLARE_ACCOUNT_ID"
        "CLOUDFLARE_API_TOKEN"
        "TWILIO_ACCOUNT_SID"
        "TWILIO_AUTH_TOKEN"
      ];
      manifest = "/integrates/secrets/development.yaml";
    };
    integratesDatabaseProd = {
      vars = [
        "CLOUDFLARE_ACCOUNT_ID"
        "CLOUDFLARE_API_TOKEN"
        "TWILIO_ACCOUNT_SID"
        "TWILIO_AUTH_TOKEN"
      ];
      manifest = "/integrates/secrets/production.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    integratesDatabase = {
      cloudflare_api_token = "CLOUDFLARE_API_TOKEN";
      twilio_account_sid = "TWILIO_ACCOUNT_SID";
      twilio_auth_token = "TWILIO_AUTH_TOKEN";
    };
  };
  testTerraform = {
    modules = {
      integratesDatabase = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/integratesDatabaseDev"
          outputs."/secretsForTerraformFromEnv/integratesDatabase"
        ];
        src = "/integrates/infra/database/src";
        version = "1.0";
      };
    };
  };
}
