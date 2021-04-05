{ nixpkgs
, makeEntrypoint
, path
, terraformApply
, ...
}:
makeEntrypoint {
  name = "makes-k8s-new-apply";
  searchPaths = {
    envPaths = [
      (terraformApply {
        name = "terraform-apply";
        product = "makes";
        target = "makes/applications/makes/k8s-new/src/terraform";
      })
      nixpkgs.curl
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/makes/k8s-new/apply/entrypoint.sh";
}
