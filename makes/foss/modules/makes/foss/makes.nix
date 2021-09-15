# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesFoss = {
        setup = [
          outputs."/secretsForTerraformFromEnv/makesFoss"
          outputs."/secretsForAwsFromEnv/makesProd"
        ];
        src = "/makes/foss/modules/makes/foss/infra";
        version = "0.14";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesFoss = {
        setup = [
          outputs."/secretsForTerraformFromEnv/makesFoss"
          outputs."/secretsForAwsFromEnv/makesDev"
        ];
        src = "/makes/foss/modules/makes/foss/infra";
        version = "0.14";
      };
    };
  };
  secretsForTerraformFromEnv = {
    makesFoss = {
      githubToken = "GITHUB_API_TOKEN";
    };
  };
  testTerraform = {
    modules = {
      makesFoss = {
        setup = [
          outputs."/secretsForTerraformFromEnv/makesFoss"
          outputs."/secretsForAwsFromEnv/makesDev"
        ];
        src = "/makes/foss/modules/makes/foss/infra";
        version = "0.14";
      };
    };
  };
}
