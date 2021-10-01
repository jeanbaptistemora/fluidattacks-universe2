# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesDns = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForEnvFromSops/makesDnsProd"
          outputs."/secretsForTerraformFromEnv/makesDns"
        ];
        src = "/makes/makes/dns/infra";
        version = "0.14";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesDns = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
          outputs."/secretsForEnvFromSops/makesDnsDev"
          outputs."/secretsForTerraformFromEnv/makesDns"
        ];
        src = "/makes/makes/dns/infra";
        version = "0.14";
      };
    };
  };
  secretsForEnvFromSops = {
    makesDnsDev = {
      vars = [ "CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL" ];
      manifest = "/makes/makes/secrets/dev.yaml";
    };
    makesDnsProd = {
      vars = [ "CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL" ];
      manifest = "/makes/makes/secrets/prod.yaml";
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
          outputs."/secretsForAwsFromEnv/makesDev"
          outputs."/secretsForEnvFromSops/makesDnsDev"
          outputs."/secretsForTerraformFromEnv/makesDns"
        ];
        src = "/makes/makes/dns/infra";
        version = "0.14";
      };
    };
  };
}
