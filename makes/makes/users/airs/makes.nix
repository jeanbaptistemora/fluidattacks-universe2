# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  lintTerraform = {
    modules = {
      makesUsersAirs = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
        ];
        src = "/makes/applications/makes/users/airs/src/terraform";
        version = "0.13";
      };
    };
  };
}
