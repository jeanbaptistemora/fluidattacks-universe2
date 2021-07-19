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
          outputs."/secretsForAwsFromEnv/makesDev"
        ];
        src = "/makes/makes/foss/infra";
        version = "0.13";
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
        src = "/makes/makes/foss/infra";
        version = "0.13";
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
        src = "/makes/makes/foss/infra";
        version = "0.13";
      };
    };
  };
}
