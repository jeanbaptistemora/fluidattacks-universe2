{ path
, integratesPkgs
, integratesPkgsTerraform
, ...
} @ attrs:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path integratesPkgs;
  terraformTest = import (path "/makes/utils/terraform-test") path integratesPkgsTerraform;
in
makeEntrypoint rec {
  arguments = {
    envTerraformTest = "${terraformTest {
      inherit name;
      product = "integrates";
      target = "integrates/deploy/secret-management/terraform";
    }}/bin/${name}";
    envUtilsMeltsLibCommon = import (path "/makes/libs/melts") attrs.copy;
  };
  name = "integrates-infra-secret-management-test";
  template = path "/makes/applications/integrates/infra/secret-management/test/entrypoint.sh";
}
