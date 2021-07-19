# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesCi = {
        setup = [ outputs."/secretsForAwsFromEnv/makesProd" ];
        src = "/makes/makes/ci/infra";
        version = "0.13";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesCi = {
        setup = [ outputs."/secretsForAwsFromEnv/makesDev" ];
        src = "/makes/makes/ci/infra";
        version = "0.13";
      };
    };
  };
  testTerraform = {
    modules = {
      makesCi = {
        setup = [ outputs."/secretsForAwsFromEnv/makesDev" ];
        src = "/makes/makes/ci/infra";
        version = "0.13";
      };
    };
  };
}
