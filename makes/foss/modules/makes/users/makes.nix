{
  imports = [
    ./dev/makes.nix
    ./infra_roles/makes.nix
    ./prod/makes/makes.nix
    ./prod/services/makes.nix
  ];
  secretsForEnvFromSops = {
    makesUsersDev = {
      vars = ["CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL"];
      manifest = "/makes/secrets/dev.yaml";
    };
    makesUsersProd = {
      vars = ["CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL"];
      manifest = "/makes/secrets/prod.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    makesUsers = {
      gitlab_token = "PRODUCT_API_TOKEN";
      gitlab_token_services = "SERVICES_API_TOKEN";
      region = "AWS_DEFAULT_REGION";
    };
  };
}
