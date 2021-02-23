{ integratesPkgs
, integratesPkgsTerraform
, makeEntrypoint
, packages
, path
, terraformApply
, ...
}:
makeEntrypoint integratesPkgs rec {
  arguments = {
    envLambdaSendMailNotification = packages.integrates.lambda.send-mail-notification;
  };
  name = "integrates-infra-resources-apply";
  searchPaths = {
    envPaths = [
      (terraformApply integratesPkgsTerraform {
        inherit name;
        product = "integrates";
        target = "integrates/deploy/terraform-resources";
      })
    ];
  };
  template = path "/makes/applications/integrates/infra/resources/apply/entrypoint.sh";
}
