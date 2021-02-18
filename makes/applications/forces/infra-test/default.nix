{ forcesPkgs
, forcesPkgsTerraform
, packages
, path
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path forcesPkgs;
  terraformTest = import (path "/makes/utils/terraform-test") path forcesPkgsTerraform;
in
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
