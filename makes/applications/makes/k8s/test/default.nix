{ nixpkgs
, makeEntrypoint
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
        product = "makes";
        target = "makes/applications/makes/k8s/src/terraform";
      })
      nixpkgs.gnugrep
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/makes/k8s/test/entrypoint.sh";
}
