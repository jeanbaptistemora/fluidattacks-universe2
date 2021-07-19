# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      ci = {
        setup = [ outputs."/secretsForAwsFromEnv/makesProd" ];
        src = "/makes/makes/ci/infra";
        version = "0.13";
      };
    };
  };
  lintTerraform = {
    modules = {
      ci = {
        setup = [ outputs."/secretsForAwsFromEnv/makesDev" ];
        src = "/makes/makes/ci/infra";
        version = "0.13";
      };
    };
  };
  testTerraform = {
    modules = {
      ci = {
        setup = [ outputs."/secretsForAwsFromEnv/makesDev" ];
        src = "/makes/makes/ci/infra";
        version = "0.13";
      };
    };
  };
}
