{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      sorts = {
        setup = [ outputs."/secretsForAwsFromEnv/sortsDev" ];
        src = "/makes/sorts/infra/infra";
        version = "0.14";
      };
    };
  };
  lintTerraform = {
    modules = {
      sorts = {
        setup = [ outputs."/secretsForAwsFromEnv/sortsDev" ];
        src = "/makes/sorts/infra/infra";
        version = "0.14";
      };
    };
  };
  testTerraform = {
    modules = {
      sorts = {
        setup = [ outputs."/secretsForAwsFromEnv/sortsDev" ];
        src = "/makes/sorts/infra/infra";
        version = "0.14";
      };
    };
  };
}
