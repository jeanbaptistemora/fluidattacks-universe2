{ packages
, path
, terraformTest
, makeEntrypoint
, ...
}:
makeEntrypoint rec {
  arguments = {
    envTerraformTest = "${terraformTest {
      inherit name;
      product = "integrates";
      target = "integrates/deploy/secret-management/terraform";
    }}/bin/${name}";
    envUtilsMeltsLibCommon = packages.melts.lib;
  };
  name = "integrates-infra-secret-management-test";
  template = path "/makes/applications/integrates/infra/secret-management/test/entrypoint.sh";
}
