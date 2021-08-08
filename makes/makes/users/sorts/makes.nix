# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesUsersSorts = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
        ];
        src = "/makes/makes/users/sorts/infra";
        version = "0.13";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesUsersSorts = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
        ];
        src = "/makes/makes/users/sorts/infra";
        version = "0.13";
      };
    };
  };
  testTerraform = {
    modules = {
      makesUsersSorts = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
        ];
        src = "/makes/makes/users/sorts/infra";
        version = "0.13";
      };
    };
  };
}
