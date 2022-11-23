{outputs, ...}: {
  deployTerraform = {
    modules = {
      integratesInfra = {
        setup = [
          outputs."/secretsForAwsFromGitlab/prodIntegrates"
          outputs."/secretsForEnvFromSops/integratesInfraProd"
          outputs."/secretsForTerraformFromEnv/integratesInfra"
        ];
        src = "/integrates/infra/src";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      integratesInfra = {
        setup = [
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/secretsForEnvFromSops/integratesInfraDev"
          outputs."/secretsForTerraformFromEnv/integratesInfra"
        ];
        src = "/integrates/infra/src";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    integratesInfraDev = {
      vars = [
        "CLOUDFLARE_ACCOUNT_ID"
        "CLOUDFLARE_API_TOKEN"
        "TWILIO_ACCOUNT_SID"
        "TWILIO_AUTH_TOKEN"
      ];
      manifest = "/integrates/secrets/development.yaml";
    };
    integratesInfraProd = {
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
    integratesInfra = {
      cloudflare_api_token = "CLOUDFLARE_API_TOKEN";
      twilio_account_sid = "TWILIO_ACCOUNT_SID";
      twilio_auth_token = "TWILIO_AUTH_TOKEN";
    };
  };
  testTerraform = {
    modules = {
      integratesInfra = {
        setup = [
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/secretsForEnvFromSops/integratesInfraDev"
          outputs."/secretsForTerraformFromEnv/integratesInfra"
        ];
        src = "/integrates/infra/src";
        version = "1.0";
      };
    };
  };
}
