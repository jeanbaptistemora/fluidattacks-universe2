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
        version = "1.0";
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
        version = "1.0";
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
        version = "1.0";
      };
    };
  };
}
