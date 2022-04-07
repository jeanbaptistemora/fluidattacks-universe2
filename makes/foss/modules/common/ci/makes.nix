# https://github.com/fluidattacks/makes
{
  inputs,
  makeSearchPaths,
  outputs,
  projectPath,
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
          outputs."/secretsForAwsFromEnv/prodMakes"
          outputs."/secretsForEnvFromSops/commonCiProd"
          outputs."/secretsForTerraformFromEnv/commonCi"
          outputs."/envVarsForTerraform/commonCi"
        ];
        src = "/makes/foss/modules/common/ci/infra";
        version = "1.0";
      };
    };
  };
  envVarsForTerraform = {
    commonCi = {
      ciInit = projectPath "/makes/foss/modules/common/ci/infra/init";
    };
  };
  lintTerraform = {
    modules = {
      commonCi = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/commonCiDev"
          outputs."/secretsForTerraformFromEnv/commonCi"
          outputs."/envVarsForTerraform/commonCi"
        ];
        src = "/makes/foss/modules/common/ci/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    commonCiProd = {
      vars = ["GITLAB_TOKEN_FLUIDATTACKS"];
      manifest = "/makes/secrets/prod.yaml";
    };
    commonCiDev = {
      vars = ["GITLAB_TOKEN_FLUIDATTACKS"];
      manifest = "/makes/secrets/dev.yaml";
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
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/commonCiDev"
          outputs."/secretsForTerraformFromEnv/commonCi"
          outputs."/envVarsForTerraform/commonCi"
        ];
        src = "/makes/foss/modules/common/ci/infra";
        version = "1.0";
      };
    };
  };
}
