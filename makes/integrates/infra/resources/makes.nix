{ inputs
, outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      integratesResources = {
        setup = [
          outputs."/envVarsForTerraform/integratesResources"
          outputs."/secretsForAwsFromEnv/integratesDev"
        ];
        src = "/makes/integrates/infra/resources/infra";
        version = "0.14";
      };
    };
  };
  envVarsForTerraform = {
    integratesResources = {
      aws_lambda_send_mail_notification_zip =
        inputs.product.integrates-lambda-send-mail-notification.outPath;
    };
  };
  lintTerraform = {
    modules = {
      integratesResources = {
        setup = [
          outputs."/envVarsForTerraform/integratesResources"
          outputs."/secretsForAwsFromEnv/integratesDev"
        ];
        src = "/makes/integrates/infra/resources/infra";
        version = "0.14";
      };
    };
  };
  testTerraform = {
    modules = {
      integratesResources = {
        setup = [
          outputs."/envVarsForTerraform/integratesResources"
          outputs."/secretsForAwsFromEnv/integratesDev"
        ];
        src = "/makes/integrates/infra/resources/infra";
        version = "0.14";
      };
    };
  };
}
