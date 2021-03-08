{ makeEntrypoint
, path
, terraformTest
, ...
}:
makeEntrypoint {
  name = "integrates-infra-cluster-test";
  searchPaths = {
    envPaths = [
      (terraformTest {
        name = "terraform-test";
        product = "integrates";
        target = "integrates/deploy/cluster/terraform";
      })
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/integrates/infra/cluster/test/entrypoint.sh";
}
