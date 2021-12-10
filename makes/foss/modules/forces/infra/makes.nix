{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      forces = {
        setup = [ outputs."/secretsForAwsFromEnv/prodForces" ];
        src = "/forces/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      forces = {
        setup = [ outputs."/secretsForAwsFromEnv/dev" ];
        src = "/forces/infra";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      forces = {
        setup = [ outputs."/secretsForAwsFromEnv/dev" ];
        src = "/forces/infra";
        version = "1.0";
      };
    };
  };
}
