{ makeEntrypoint
, path
, terraformApply
, ...
}:
makeEntrypoint {
  name = "makes-k8s-apply";
  searchPaths = {
    envPaths = [
      (terraformApply {
        name = "terraform-apply";
        product = "integrates";
        target = "makes/applications/makes/k8s/src/terraform";
      })
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/makes/k8s/apply/entrypoint.sh";
}
