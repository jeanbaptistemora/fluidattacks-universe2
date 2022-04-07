# https://github.com/fluidattacks/makes
{outputs, ...}: {
  deployTerraform = {
    modules = {
      makesFoss = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodMakes"
          outputs."/secretsForEnvFromSops/makesFossProd"
          outputs."/secretsForTerraformFromEnv/makesFoss"
        ];
        src = "/makes/foss/modules/common/foss/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesFoss = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/makesFossDev"
          outputs."/secretsForTerraformFromEnv/makesFoss"
        ];
        src = "/makes/foss/modules/common/foss/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    makesFossDev = {
      vars = ["GITHUB_API_TOKEN"];
      manifest = "/makes/secrets/dev.yaml";
    };
    makesFossProd = {
      vars = ["GITHUB_API_TOKEN"];
      manifest = "/makes/secrets/prod.yaml";
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
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/makesFossDev"
          outputs."/secretsForTerraformFromEnv/makesFoss"
        ];
        src = "/makes/foss/modules/common/foss/infra";
        version = "1.0";
      };
    };
  };
}
