{
  imports = [
    ./dev/makes.nix
    ./makes/makes.nix
    ./melts/makes.nix
    ./observes/makes.nix
    ./prod/airs/makes.nix
    ./prod/docs/makes.nix
    ./prod/forces/makes.nix
    ./prod/integrates/makes.nix
    ./services/makes.nix
    ./skims/makes.nix
    ./sorts/makes.nix
  ];
  secretsForEnvFromSops = {
    makesUsersDev = {
      vars = [ "CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL" ];
      manifest = "/makes/foss/modules/makes/secrets/dev.yaml";
    };
    makesUsersProd = {
      vars = [ "CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL" ];
      manifest = "/makes/foss/modules/makes/secrets/prod.yaml";
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
