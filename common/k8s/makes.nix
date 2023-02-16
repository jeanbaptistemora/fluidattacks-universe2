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
      commonK8s = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromGitlab/prodCommon"
          outputs."/secretsForEnvFromSops/commonCloudflareProd"
          outputs."/secretsForEnvFromSops/commonK8sProd"
          outputs."/secretsForTerraformFromEnv/commonK8s"
        ];
        src = "/common/k8s/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      commonK8s = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/secretsForEnvFromSops/commonCloudflareDev"
          outputs."/secretsForEnvFromSops/commonK8sDev"
          outputs."/secretsForTerraformFromEnv/commonK8s"
        ];
        src = "/common/k8s/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    commonK8sDev = {
      vars = ["NEW_RELIC_LICENSE_KEY"];
      manifest = "/common/secrets/dev.yaml";
    };
    commonK8sProd = {
      vars = ["NEW_RELIC_LICENSE_KEY"];
      manifest = "/common/secrets/prod.yaml";
    };
  };
  secretsForKubernetesConfigFromAws = {
    commonK8s = {
      cluster = "common-k8s";
      region = "us-east-1";
    };
  };
  secretsForTerraformFromEnv = {
    commonK8s = {
      cloudflareApiKey = "CLOUDFLARE_API_KEY";
      cloudflareEmail = "CLOUDFLARE_EMAIL";
      newRelicLicenseKey = "NEW_RELIC_LICENSE_KEY";
    };
  };
  secureKubernetesWithRbacPolice = {
    commonK8s = {
      severity = "Low";
      setup = [
        outputs."/secretsForAwsFromGitlab/prodCommon"
        outputs."/secretsForKubernetesConfigFromAws/commonK8s"
      ];
    };
  };
  testTerraform = {
    modules = {
      commonK8s = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/secretsForEnvFromSops/commonCloudflareDev"
          outputs."/secretsForEnvFromSops/commonK8sDev"
          outputs."/secretsForTerraformFromEnv/commonK8s"
        ];
        src = "/common/k8s/infra";
        version = "1.0";
      };
    };
  };
}
