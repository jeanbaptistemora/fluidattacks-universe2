# https://github.com/fluidattacks/makes
{ inputs
, makeSearchPaths
, outputs
, ...
}:
let
  searchPaths = makeSearchPaths {
    bin = [ inputs.nixpkgs.git ];
  };
in
{
  lintTerraform = {
    modules = {
      makesKubernetes = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/makesDev"
          outputs."/secretsForEnvFromSops/makesKubernetesDev"
          outputs."/secretsForTerraformFromEnv/makesKubernetes"
        ];
        src = "/makes/applications/makes/k8s/src/terraform";
        version = "0.13";
      };
    };
  };
  secretsForEnvFromSops = {
    makesKubernetesDev = {
      vars = [ "CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL" ];
      manifest = "/makes/makes/secrets/dev.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    makesKubernetes = {
      cloudflareApiKey = "CLOUDFLARE_API_KEY";
      cloudflareEmail = "CLOUDFLARE_EMAIL";
    };
  };
}
