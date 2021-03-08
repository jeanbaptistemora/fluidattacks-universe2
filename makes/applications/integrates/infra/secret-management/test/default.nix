{ packages
, path
, terraformTest
, makeEntrypoint
, ...
}:
makeEntrypoint {
  name = "integrates-infra-secret-management-test";
  searchPaths = {
    envPaths = [
      (terraformTest {
        name = "terraform-test";
        product = "integrates";
        target = "integrates/deploy/secret-management/terraform";
      })
    ];
    envSources = [
      packages.melts.lib
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/integrates/infra/secret-management/test/entrypoint.sh";
}
