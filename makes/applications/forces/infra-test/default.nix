{ terraformTest
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint rec {
  arguments = {
    envTerraformTest = "${terraformTest {
      inherit name;
      product = "forces";
      target = "forces/infra";
    }}/bin/${name}";
    envUtilsMeltsLibCommon = packages.melts.lib;
  };
  name = "forces-infra-test";
  template = path "/makes/applications/forces/infra-test/entrypoint.sh";
}
