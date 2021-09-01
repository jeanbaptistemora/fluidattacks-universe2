{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      integratesSecrets = {
        setup = [ outputs."/secretsForAwsFromEnv/integratesDev" ];
        src = "/makes/integrates/infra/secrets/infra";
        version = "0.14";
      };
    };
  };
  lintTerraform = {
    modules = {
      integratesSecrets = {
        setup = [ outputs."/secretsForAwsFromEnv/integratesDev" ];
        src = "/makes/integrates/infra/secrets/infra";
        version = "0.14";
      };
    };
  };
  testTerraform = {
    modules = {
      integratesSecrets = {
        setup = [ outputs."/secretsForAwsFromEnv/integratesDev" ];
        src = "/makes/integrates/infra/secrets/infra";
        version = "0.14";
      };
    };
  };
}
