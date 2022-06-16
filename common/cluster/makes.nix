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
      commonCluster = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/prodCommon"
          outputs."/secretsForEnvFromSops/commonClusterProd"
          outputs."/secretsForKubernetesConfigFromAws/commonCluster"
          outputs."/secretsForTerraformFromEnv/commonCluster"
        ];
        src = "/common/cluster/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      commonCluster = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/commonClusterDev"
          outputs."/secretsForTerraformFromEnv/commonCluster"
        ];
        src = "/common/cluster/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    commonClusterDev = {
      vars = [
        "CLOUDFLARE_ACCOUNT_ID"
        "CLOUDFLARE_API_KEY"
        "CLOUDFLARE_EMAIL"
        "NEW_RELIC_LICENSE_KEY"
      ];
      manifest = "/common/secrets/dev.yaml";
    };
    commonClusterProd = {
      vars = [
        "CLOUDFLARE_ACCOUNT_ID"
        "CLOUDFLARE_API_KEY"
        "CLOUDFLARE_EMAIL"
        "NEW_RELIC_LICENSE_KEY"
      ];
      manifest = "/common/secrets/prod.yaml";
    };
  };
  secretsForKubernetesConfigFromAws = {
    commonCluster = {
      cluster = "makes-k8s";
      region = "us-east-1";
    };
  };
  secretsForTerraformFromEnv = {
    commonCluster = {
      cloudflareApiKey = "CLOUDFLARE_API_KEY";
      cloudflareEmail = "CLOUDFLARE_EMAIL";
      newRelicLicenseKey = "NEW_RELIC_LICENSE_KEY";
      kubeConfig = "KUBECONFIG";
    };
  };
  testTerraform = {
    modules = {
      commonCluster = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/commonClusterDev"
          outputs."/secretsForKubernetesConfigFromAws/commonCluster"
          outputs."/secretsForTerraformFromEnv/commonCluster"
        ];
        src = "/common/cluster/infra";
        version = "1.0";
      };
    };
  };
}
