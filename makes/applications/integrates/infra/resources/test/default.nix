{ integratesPkgs
, integratesPkgsTerraform
, makeEntrypoint
, packages
, path
, terraformTest
, ...
}:
makeEntrypoint integratesPkgs rec {
  arguments = {
    envLambdaSendMailNotification = packages.integrates.lambda.send-mail-notification;
  };
  name = "integrates-infra-resources-test";
  searchPaths = {
    envPaths = [
      (terraformTest integratesPkgsTerraform {
        inherit name;
        product = "integrates";
        target = "integrates/deploy/terraform-resources";
      })
    ];
  };
  template = path "/makes/applications/integrates/infra/resources/test/entrypoint.sh";
}
