# https://github.com/fluidattacks/makes
{ inputs
, makeSearchPaths
, outputs
, projectPath
, ...
}:
let
  searchPaths = makeSearchPaths {
    bin = [
      inputs.nixpkgs.awscli
      inputs.nixpkgs.bash
      inputs.nixpkgs.git
      inputs.nixpkgs.jq
    ];
  };
in
{
  deployTerraform = {
    modules = {
      makesCi = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/prodMakes"
          outputs."/secretsForEnvFromSops/makesCiProd"
          outputs."/secretsForTerraformFromEnv/makesCi"
          outputs."/envVarsForTerraform/makesCi"
        ];
        src = "/makes/foss/modules/makes/ci/infra";
        version = "1.0";
      };
    };
  };
  envVarsForTerraform = {
    makesCi = {
      makesCiInit = projectPath "/makes/foss/modules/makes/ci/infra/init";
    };
  };
  lintTerraform = {
    modules = {
      makesCi = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/makesCiDev"
          outputs."/secretsForTerraformFromEnv/makesCi"
          outputs."/envVarsForTerraform/makesCi"
        ];
        src = "/makes/foss/modules/makes/ci/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    makesCiProd = {
      vars = [
        "GITLAB_TOKEN_FLUIDATTACKS"
        "GITLAB_TOKEN_AUTONOMICMIND"
        "GITLAB_TOKEN_AUTONOMICJUMP"
      ];
      manifest = "/makes/secrets/prod.yaml";
    };
    makesCiDev = {
      vars = [
        "GITLAB_TOKEN_FLUIDATTACKS"
        "GITLAB_TOKEN_AUTONOMICMIND"
        "GITLAB_TOKEN_AUTONOMICJUMP"
      ];
      manifest = "/makes/secrets/dev.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    makesCi = {
      gitlabTokenFluidattacks = "GITLAB_TOKEN_FLUIDATTACKS";
      gitlabTokenAutonomicmind = "GITLAB_TOKEN_AUTONOMICMIND";
      gitlabTokenAutonomicjump = "GITLAB_TOKEN_AUTONOMICJUMP";
    };
  };
  testTerraform = {
    modules = {
      makesCi = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/makesCiDev"
          outputs."/secretsForTerraformFromEnv/makesCi"
          outputs."/envVarsForTerraform/makesCi"
        ];
        src = "/makes/foss/modules/makes/ci/infra";
        version = "1.0";
      };
    };
  };
}
