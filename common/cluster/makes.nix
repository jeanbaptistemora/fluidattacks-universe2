# https://github.com/fluidattacks/makes
{
  inputs,
  makeSearchPaths,
  outputs,
  ...
}: let
  searchPaths = makeSearchPaths {
    bin = [
      inputs.nixpkgs.awscli
      inputs.nixpkgs.git
    ];
  };
in {
  deployTerraform = {
    modules = {
      commonCluster = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromGitlab/prodCommon"
          outputs."/secretsForEnvFromSops/commonCloudflareProd"
          outputs."/secretsForEnvFromSops/commonClusterProd"
          outputs."/secretsForTerraformFromEnv/commonCluster"
        ];
        src = "/common/cluster/infra";
        version = "1.0";
      };
      commonClusterNew = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromGitlab/prodCommon"
          outputs."/secretsForEnvFromSops/commonCloudflareProd"
          outputs."/secretsForEnvFromSops/commonClusterProd"
          outputs."/secretsForTerraformFromEnv/commonCluster"
        ];
        src = "/common/cluster/new";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      commonCluster = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/secretsForEnvFromSops/commonCloudflareDev"
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
      vars = ["NEW_RELIC_LICENSE_KEY"];
      manifest = "/common/secrets/dev.yaml";
    };
    commonClusterProd = {
      vars = ["NEW_RELIC_LICENSE_KEY"];
      manifest = "/common/secrets/prod.yaml";
    };
  };
  secretsForKubernetesConfigFromAws = {
    commonCluster = {
      cluster = "common";
      region = "us-east-1";
    };
  };
  secretsForTerraformFromEnv = {
    commonCluster = {
      cloudflareApiKey = "CLOUDFLARE_API_KEY";
      cloudflareEmail = "CLOUDFLARE_EMAIL";
      newRelicLicenseKey = "NEW_RELIC_LICENSE_KEY";
    };
  };
  secureKubernetesWithRbacPolice = {
    commonCluster = {
      severity = "Low";
      setup = [
        outputs."/secretsForAwsFromGitlab/prodCommon"
        outputs."/secretsForKubernetesConfigFromAws/commonCluster"
      ];
    };
  };
  testTerraform = {
    modules = {
      commonCluster = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/secretsForEnvFromSops/commonCloudflareDev"
          outputs."/secretsForEnvFromSops/commonClusterDev"
          outputs."/secretsForTerraformFromEnv/commonCluster"
        ];
        src = "/common/cluster/infra";
        version = "1.0";
      };
    };
  };
}
