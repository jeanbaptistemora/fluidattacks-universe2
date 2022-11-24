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
      inputs.nixpkgs.bash
      inputs.nixpkgs.git
      inputs.nixpkgs.jq
    ];
  };
in {
  deployTerraform = {
    modules = {
      commonCi = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromGitlab/prodCommon"
          outputs."/secretsForEnvFromSops/commonCiProd"
          outputs."/secretsForTerraformFromEnv/commonCi"
        ];
        src = "/common/ci/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      commonCi = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/secretsForEnvFromSops/commonCiDev"
          outputs."/secretsForTerraformFromEnv/commonCi"
        ];
        src = "/common/ci/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    commonCiProd = {
      vars = [
        "GITLAB_TOKEN_FLUIDATTACKS"
      ];
      manifest = "/common/secrets/prod.yaml";
    };
    commonCiDev = {
      vars = [
        "GITLAB_TOKEN_FLUIDATTACKS"
      ];
      manifest = "/common/secrets/dev.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    commonCi = {
      gitlabTokenFluidattacks = "GITLAB_TOKEN_FLUIDATTACKS";
    };
  };
  testTerraform = {
    modules = {
      commonCi = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromGitlab/dev"
          outputs."/secretsForEnvFromSops/commonCiDev"
          outputs."/secretsForTerraformFromEnv/commonCi"
        ];
        src = "/common/ci/infra";
        version = "1.0";
      };
    };
  };
}
