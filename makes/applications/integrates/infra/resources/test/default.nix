{ makeEntrypoint
, packages
, path
, terraformTest
, ...
}:
makeEntrypoint {
  arguments = {
    envLambdaSendMailNotification = packages.integrates.lambda.send-mail-notification;
  };
  name = "integrates-infra-resources-test";
  searchPaths = {
    envPaths = [
      (terraformTest {
        name = "terraform-test";
        product = "integrates";
        target = "integrates/deploy/terraform-resources";
      })
    ];
  };
  template = path "/makes/applications/integrates/infra/resources/test/entrypoint.sh";
}
