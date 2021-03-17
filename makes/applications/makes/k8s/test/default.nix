{ makeEntrypoint
, path
, terraformTest
, ...
}:
makeEntrypoint {
  name = "makes-k8s-test";
  searchPaths = {
    envPaths = [
      (terraformTest {
        name = "terraform-test";
        product = "integrates";
        target = "makes/applications/makes/k8s/src/terraform";
      })
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/makes/k8s/test/entrypoint.sh";
}
