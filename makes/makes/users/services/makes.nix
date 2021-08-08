# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesUsersServices = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
        ];
        src = "/makes/makes/users/services/infra";
        version = "0.13";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesUsersServices = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
        ];
        src = "/makes/makes/users/services/infra";
        version = "0.13";
      };
    };
  };
  testTerraform = {
    modules = {
      makesUsersServices = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
        ];
        src = "/makes/makes/users/services/infra";
        version = "0.13";
      };
    };
  };
}
