{outputs, ...}: {
  deployTerraform = {
    modules = {
      integratesResources = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodIntegrates"
          outputs."/secretsForEnvFromSops/integratesResourcesProd"
          outputs."/secretsForTerraformFromEnv/integratesResources"
        ];
        src = "/integrates/infra/resources/src";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      integratesResources = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/integratesResourcesDev"
          outputs."/secretsForTerraformFromEnv/integratesResources"
        ];
        src = "/integrates/infra/resources/src";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    integratesResourcesDev = {
      vars = ["TWILIO_ACCOUNT_SID" "TWILIO_AUTH_TOKEN"];
      manifest = "/integrates/secrets-development.yaml";
    };
    integratesResourcesProd = {
      vars = ["TWILIO_ACCOUNT_SID" "TWILIO_AUTH_TOKEN"];
      manifest = "/integrates/secrets-production.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    integratesResources = {
      twilio_account_sid = "TWILIO_ACCOUNT_SID";
      twilio_auth_token = "TWILIO_AUTH_TOKEN";
    };
  };
  testTerraform = {
    modules = {
      integratesResources = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/integratesResourcesDev"
          outputs."/secretsForTerraformFromEnv/integratesResources"
        ];
        src = "/integrates/infra/resources/src";
        version = "1.0";
      };
    };
  };
}
