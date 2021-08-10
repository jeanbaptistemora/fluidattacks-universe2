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
      vars = [ "FLUID_ATTACKS_TOKEN" ];
      manifest = "/makes/makes/secrets/prod.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    makesCiProd = {
      fluidAttacksToken = "FLUID_ATTACKS_TOKEN";
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
