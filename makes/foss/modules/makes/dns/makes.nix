# https://github.com/fluidattacks/makes
{outputs, ...}: {
  deployTerraform = {
    modules = {
      makesDns = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodMakes"
          outputs."/secretsForEnvFromSops/makesDnsProd"
          outputs."/secretsForTerraformFromEnv/makesDns"
        ];
        src = "/makes/foss/modules/makes/dns/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesDns = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/makesDnsDev"
          outputs."/secretsForTerraformFromEnv/makesDns"
        ];
        src = "/makes/foss/modules/makes/dns/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    makesDnsDev = {
      vars = ["CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL"];
      manifest = "/makes/secrets/dev.yaml";
    };
    makesDnsProd = {
      vars = ["CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL"];
      manifest = "/makes/secrets/prod.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    makesDns = {
      cloudflareApiKey = "CLOUDFLARE_API_KEY";
      cloudflareEmail = "CLOUDFLARE_EMAIL";
    };
  };
  testTerraform = {
    modules = {
      makesDns = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/makesDnsDev"
          outputs."/secretsForTerraformFromEnv/makesDns"
        ];
        src = "/makes/foss/modules/makes/dns/infra";
        version = "1.0";
      };
    };
  };
}
