# https://github.com/fluidattacks/makes
{
  inputs,
  makeSearchPaths,
  outputs,
  ...
}: let
  searchPaths = makeSearchPaths {
    bin = [inputs.nixpkgs.git];
  };
in {
  deployTerraform = {
    modules = {
      makesKubernetes = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/prodMakes"
          outputs."/secretsForEnvFromSops/makesKubernetesProd"
          outputs."/secretsForKubernetesConfigFromAws/makesKubernetes"
          outputs."/secretsForTerraformFromEnv/makesKubernetes"
        ];
        src = "/makes/foss/modules/makes/kubernetes/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesKubernetes = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/makesKubernetesDev"
          outputs."/secretsForTerraformFromEnv/makesKubernetes"
        ];
        src = "/makes/foss/modules/makes/kubernetes/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    makesKubernetesDev = {
      vars = [
        "CLOUDFLARE_ACCOUNT_ID"
        "CLOUDFLARE_API_KEY"
        "CLOUDFLARE_EMAIL"
        "NEW_RELIC_LICENSE_KEY"
        "NEW_RELIC_PIXIE_API_KEY"
        "NEW_RELIC_PIXIE_DEPLOY_KEY"
      ];
      manifest = "/makes/secrets/dev.yaml";
    };
    makesKubernetesProd = {
      vars = [
        "CLOUDFLARE_ACCOUNT_ID"
        "CLOUDFLARE_API_KEY"
        "CLOUDFLARE_EMAIL"
        "NEW_RELIC_LICENSE_KEY"
        "NEW_RELIC_PIXIE_API_KEY"
        "NEW_RELIC_PIXIE_DEPLOY_KEY"
      ];
      manifest = "/makes/secrets/prod.yaml";
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
      newRelicLicenseKey = "NEW_RELIC_LICENSE_KEY";
      newRelicPixieApiKey = "NEW_RELIC_PIXIE_API_KEY";
      newRelicPixieDeployKey = "NEW_RELIC_PIXIE_DEPLOY_KEY";
      kubeConfig = "KUBECONFIG";
    };
  };
  testTerraform = {
    modules = {
      makesKubernetes = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/makesKubernetesDev"
          outputs."/secretsForKubernetesConfigFromAws/makesKubernetes"
          outputs."/secretsForTerraformFromEnv/makesKubernetes"
        ];
        src = "/makes/foss/modules/makes/kubernetes/infra";
        version = "1.0";
      };
    };
  };
}
