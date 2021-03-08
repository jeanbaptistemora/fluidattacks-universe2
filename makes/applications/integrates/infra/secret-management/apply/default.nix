{ packages
, makeEntrypoint
, path
, terraformApply
, ...
}:
makeEntrypoint rec {
  name = "integrates-infra-secret-management-apply";
  searchPaths = {
    envPaths = [
      (terraformApply {
        name = "terraform-apply";
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
  template = path "/makes/applications/integrates/infra/secret-management/apply/entrypoint.sh";
}
