# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      ci = {
        authentication = [ outputs."/secretsForAwsFromEnv/makesProd" ];
        src = "/makes/makes/ci/infra";
        version = "0.13";
      };
    };
  };
  lintTerraform = {
    modules = {
      ci = {
        authentication = [ outputs."/secretsForAwsFromEnv/makesDev" ];
        src = "/makes/makes/ci/infra";
        version = "0.13";
      };
    };
  };
  testTerraform = {
    modules = {
      ci = {
        authentication = [ outputs."/secretsForAwsFromEnv/makesDev" ];
        src = "/makes/makes/ci/infra";
        version = "0.13";
      };
    };
  };
}
