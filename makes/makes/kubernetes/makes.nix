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
  deployTerraform = {
    modules = {
      makesKubernetes = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForEnvFromSops/makesKubernetesProd"
          outputs."/secretsForKubernetesConfigFromAws/makesKubernetes"
          outputs."/secretsForTerraformFromEnv/makesKubernetes"
        ];
        src = "/makes/makes/kubernetes/infra";
        version = "0.14";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesKubernetes = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/makesDev"
          outputs."/secretsForEnvFromSops/makesKubernetesDev"
          outputs."/secretsForTerraformFromEnv/makesKubernetes"
        ];
        src = "/makes/makes/kubernetes/infra";
        version = "0.14";
      };
    };
  };
  secretsForEnvFromSops = {
    makesKubernetesDev = {
      vars = [ "CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL" ];
      manifest = "/makes/makes/secrets/dev.yaml";
    };
    makesKubernetesProd = {
      vars = [ "CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL" ];
      manifest = "/makes/makes/secrets/prod.yaml";
    };
  };
  secretsForKubernetesConfigFromAws = {
    makesKubernetes = {
      cluster = "makes-k8s";
      region = "us-east-1";
    };
  };
  secretsForTerraformFromEnv = {
    makesKubernetes = {
      cloudflareApiKey = "CLOUDFLARE_API_KEY";
      cloudflareEmail = "CLOUDFLARE_EMAIL";
      kubeConfig = "KUBECONFIG";
    };
  };
  testTerraform = {
    modules = {
      makesKubernetes = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/makesDev"
          outputs."/secretsForEnvFromSops/makesKubernetesDev"
          outputs."/secretsForKubernetesConfigFromAws/makesKubernetes"
          outputs."/secretsForTerraformFromEnv/makesKubernetes"
        ];
        src = "/makes/makes/kubernetes/infra";
        version = "0.14";
      };
    };
  };
}
