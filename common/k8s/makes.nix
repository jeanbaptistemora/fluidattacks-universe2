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
          outputs."/secretsForTerraformFromEnv/commonK8s"
        ];
        src = "/common/k8s/infra";
        version = "1.0";
      };
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
          outputs."/secretsForTerraformFromEnv/commonK8s"
        ];
        src = "/common/k8s/infra";
        version = "1.0";
      };
    };
  };
}
