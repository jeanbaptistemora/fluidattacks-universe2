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
          outputs."/secretsForAwsFromEnv/prodCommon"
          outputs."/secretsForEnvFromSops/commonCloudflareProd"
          outputs."/secretsForEnvFromSops/commonKubernetesProd"
          outputs."/secretsForKubernetesConfigFromAws/commonKubernetes"
          outputs."/secretsForTerraformFromEnv/commonKubernetes"
        ];
        src = "/common/kubernetes/infra";
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
          outputs."/secretsForEnvFromSops/commonCloudflareDev"
          outputs."/secretsForEnvFromSops/commonKubernetesDev"
          outputs."/secretsForTerraformFromEnv/commonKubernetes"
        ];
        src = "/common/kubernetes/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    commonKubernetesDev = {
      vars = ["NEW_RELIC_LICENSE_KEY"];
      manifest = "/common/secrets/dev.yaml";
    };
    commonKubernetesProd = {
      vars = ["NEW_RELIC_LICENSE_KEY"];
      manifest = "/common/secrets/prod.yaml";
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
      newRelicLicenseKey = "NEW_RELIC_LICENSE_KEY";
      kubeConfig = "KUBECONFIG";
    };
  };
  testTerraform = {
    modules = {
      commonKubernetes = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/commonCloudflareDev"
          outputs."/secretsForEnvFromSops/commonKubernetesDev"
          outputs."/secretsForKubernetesConfigFromAws/commonKubernetes"
          outputs."/secretsForTerraformFromEnv/commonKubernetes"
        ];
        src = "/common/kubernetes/infra";
        version = "1.0";
      };
    };
  };
}
