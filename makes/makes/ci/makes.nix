# https://github.com/fluidattacks/makes
{ inputs
, makeSearchPaths
, outputs
, ...
}:
let
  searchPaths = makeSearchPaths {
    bin = [
      inputs.nixpkgs.awscli
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
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForEnvFromSops/makesCiProd"
          outputs."/secretsForTerraformFromEnv/makesCiProd"
        ];
        src = "/makes/makes/ci/infra";
        version = "0.14";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesCi = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/makesDev"
        ];
        src = "/makes/makes/ci/infra";
        version = "0.14";
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
      manifest = "/makes/makes/secrets/prod.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    makesCiProd = {
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
          outputs."/secretsForAwsFromEnv/makesDev"
        ];
        src = "/makes/makes/ci/infra";
        version = "0.14";
      };
    };
  };
}
