{ integratesPkgs
, integratesPkgsTerraform
, path
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path integratesPkgs;
  terraformApply = import (path "/makes/utils/terraform-apply") path integratesPkgsTerraform;
in
makeEntrypoint rec {
  arguments = {
    envUtilsAws = import (path "/makes/utils/aws") path integratesPkgs;
    envUtilsSops = import (path "/makes/utils/sops") path integratesPkgs;
    envTerraformApply = "${terraformApply {
      inherit name;
      product = "integrates";
      target = "integrates/deploy/front/terraform";
    }}/bin/${name}";
  };
  name = "integrates-infra-front-apply";
  template = path "/makes/applications/integrates/infra-front-apply/entrypoint.sh";
}
