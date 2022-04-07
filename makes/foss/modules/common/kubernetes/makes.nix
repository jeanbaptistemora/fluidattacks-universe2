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
      commonKubernetes = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/prodMakes"
          outputs."/secretsForEnvFromSops/commonKubernetesProd"
          outputs."/secretsForKubernetesConfigFromAws/commonKubernetes"
          outputs."/secretsForTerraformFromEnv/commonKubernetes"
        ];
        src = "/makes/foss/modules/common/kubernetes/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      commonKubernetes = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/commonKubernetesDev"
          outputs."/secretsForTerraformFromEnv/commonKubernetes"
        ];
        src = "/makes/foss/modules/common/kubernetes/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    commonKubernetesDev = {
      vars = [
        "CLOUDFLARE_ACCOUNT_ID"
        "CLOUDFLARE_API_KEY"
        "CLOUDFLARE_EMAIL"
      ];
      manifest = "/makes/secrets/dev.yaml";
    };
    commonKubernetesProd = {
      vars = [
        "CLOUDFLARE_ACCOUNT_ID"
        "CLOUDFLARE_API_KEY"
        "CLOUDFLARE_EMAIL"
      ];
      manifest = "/makes/secrets/prod.yaml";
    };
  };
  secretsForKubernetesConfigFromAws = {
    commonKubernetes = {
      cluster = "makes-k8s";
      region = "us-east-1";
    };
  };
  secretsForTerraformFromEnv = {
    commonKubernetes = {
      cloudflareApiKey = "CLOUDFLARE_API_KEY";
      cloudflareEmail = "CLOUDFLARE_EMAIL";
      kubeConfig = "KUBECONFIG";
    };
  };
  testTerraform = {
    modules = {
      commonKubernetes = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/commonKubernetesDev"
          outputs."/secretsForKubernetesConfigFromAws/commonKubernetes"
          outputs."/secretsForTerraformFromEnv/commonKubernetes"
        ];
        src = "/makes/foss/modules/common/kubernetes/infra";
        version = "1.0";
      };
    };
  };
}
