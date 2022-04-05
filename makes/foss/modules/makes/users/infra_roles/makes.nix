# https://github.com/fluidattacks/makes
{outputs, ...}: {
  deployTerraform = {
    modules = {
      makesRolesForProjects = {
        setup = [
          outputs."/integrates/back/tools/dump-groups"
        ];
        src = "/makes/foss/modules/makes/users/prod/integrates/infra_roles";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      makesRolesForProjects = {
        setup = [
          outputs."/integrates/back/tools/dump-groups"
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/makesUsersDev"
          outputs."/secretsForTerraformFromEnv/makesUsers"
        ];
        src = "/makes/foss/modules/makes/users/prod/integrates/infra_roles";
        version = "1.0";
      };
    };
  };
}
