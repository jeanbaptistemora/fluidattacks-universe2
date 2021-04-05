{ makeEntrypoint
, path
, terraformTest
, ...
}:
makeEntrypoint {
  name = "makes-k8s-new-test";
  searchPaths = {
    envPaths = [
      (terraformTest {
        name = "terraform-test";
        product = "makes";
        target = "makes/applications/makes/k8s-new/src/terraform";
      })
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/makes/k8s-new/test/entrypoint.sh";
}
