{ makeEntrypoint
, path
, terraformApply
, ...
}:
makeEntrypoint rec {
  name = "integrates-infra-cluster-apply";
  searchPaths = {
    envPaths = [
      (terraformApply {
        name = "terraform-apply";
        product = "integrates";
        target = "integrates/deploy/cluster/terraform";
      })
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/integrates/infra/cluster/apply/entrypoint.sh";
}
