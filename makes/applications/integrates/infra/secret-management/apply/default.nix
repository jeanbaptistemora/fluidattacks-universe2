{ packages
, makeEntrypoint
, path
, terraformApply
, ...
}:
makeEntrypoint rec {
  arguments = {
    envTerraformApply = "${terraformApply {
      inherit name;
      product = "integrates";
      target = "integrates/deploy/secret-management/terraform";
    }}/bin/${name}";
    envUtilsMeltsLibCommon = packages.melts.lib;
  };
  name = "integrates-infra-secret-management-apply";
  template = path "/makes/applications/integrates/infra/secret-management/apply/entrypoint.sh";
}
