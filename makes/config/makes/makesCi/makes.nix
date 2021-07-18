# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesCi = {
        authentication = [ outputs."/secretsForAwsFromEnv/makesProd" ];
        src = "/makes/applications/makes/ci/src/terraform";
        version = "0.13";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesCi = {
        authentication = [ outputs."/secretsForAwsFromEnv/makesDev" ];
        src = "/makes/applications/makes/ci/src/terraform";
        version = "0.13";
      };
    };
  };
  testTerraform = {
    modules = {
      makesCi = {
        authentication = [ outputs."/secretsForAwsFromEnv/makesDev" ];
        src = "/makes/applications/makes/ci/src/terraform";
        version = "0.13";
      };
    };
  };
}
