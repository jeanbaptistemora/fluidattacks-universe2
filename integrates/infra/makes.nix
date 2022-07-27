{
  inputs,
  makeSearchPaths,
  outputs,
  projectPath,
  ...
}: let
  searchPaths = makeSearchPaths {
    bin = [
      inputs.nixpkgs.python39
    ];
  };
in {
  deployTerraform = {
    modules = {
      integratesInfra = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/prodIntegrates"
          outputs."/secretsForEnvFromSops/integratesInfraProd"
          outputs."/secretsForTerraformFromEnv/integratesInfra"
          outputs."/envVarsForTerraform/lambda"
        ];
        src = "/integrates/infra/src";
        version = "1.0";
      };
    };
  };
  envVarsForTerraform = {
    lambda = {
      lambda_path = projectPath "/integrates/lambda";
    };
  };
  lintTerraform = {
    modules = {
      integratesInfra = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/integratesInfraDev"
          outputs."/secretsForTerraformFromEnv/integratesInfra"
          outputs."/envVarsForTerraform/lambda"
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
          searchPaths
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/integratesInfraDev"
          outputs."/secretsForTerraformFromEnv/integratesInfra"
          outputs."/envVarsForTerraform/lambda"
        ];
        src = "/integrates/infra/src";
        version = "1.0";
      };
    };
  };
}
