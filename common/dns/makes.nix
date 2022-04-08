# https://github.com/fluidattacks/makes
{outputs, ...}: {
  deployTerraform = {
    modules = {
      commonDns = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodCommon"
          outputs."/secretsForEnvFromSops/commonDnsProd"
          outputs."/secretsForTerraformFromEnv/commonDns"
        ];
        src = "/common/dns/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      commonDns = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/commonDnsDev"
          outputs."/secretsForTerraformFromEnv/commonDns"
        ];
        src = "/common/dns/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    commonDnsDev = {
      vars = ["CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL"];
      manifest = "/makes/secrets/dev.yaml";
    };
    commonDnsProd = {
      vars = ["CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL"];
      manifest = "/makes/secrets/prod.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    commonDns = {
      cloudflareApiKey = "CLOUDFLARE_API_KEY";
      cloudflareEmail = "CLOUDFLARE_EMAIL";
    };
  };
  testTerraform = {
    modules = {
      commonDns = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/commonDnsDev"
          outputs."/secretsForTerraformFromEnv/commonDns"
        ];
        src = "/common/dns/infra";
        version = "1.0";
      };
    };
  };
}
