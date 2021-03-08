{ makeEntrypoint
, packages
, path
, terraformApply
, ...
}:
makeEntrypoint {
  arguments = {
    envLambdaSendMailNotification = packages.integrates.lambda.send-mail-notification;
  };
  name = "integrates-infra-resources-apply";
  searchPaths = {
    envPaths = [
      (terraformApply {
        name = "terraform-apply";
        product = "integrates";
        target = "integrates/deploy/terraform-resources";
      })
    ];
  };
  template = path "/makes/applications/integrates/infra/resources/apply/entrypoint.sh";
}
