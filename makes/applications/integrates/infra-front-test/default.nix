{ integratesPkgs
, integratesPkgsTerraform
, path
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path integratesPkgs;
  terraformTest = import (path "/makes/utils/terraform-test") path integratesPkgsTerraform;
in
makeEntrypoint rec {
  arguments = {
    envUtilsAws = import (path "/makes/utils/aws") path integratesPkgs;
    envUtilsSops = import (path "/makes/utils/sops") path integratesPkgs;
    envTerraformTest = "${terraformTest {
      inherit name;
      product = "integrates";
      target = "integrates/deploy/front/terraform";
    }}/bin/${name}";
  };
  name = "integrates-infra-front-test";
  template = path "/makes/applications/integrates/infra-front-test/entrypoint.sh";
}
