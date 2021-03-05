{ makeEntrypoint
, packages
, path
, terraformApply
, ...
}:
makeEntrypoint rec {
  arguments = {
    envTerraformApply = "${terraformApply {
      inherit name;
      product = "forces";
      target = "forces/infra";
    }}/bin/${name}";
    envUtilsMeltsLibCommon = packages.melts.lib;
  };
  name = "forces-infra-apply";
  template = path "/makes/applications/forces/infra-apply/entrypoint.sh";
}
