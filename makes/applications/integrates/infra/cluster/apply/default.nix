{ integratesPkgs
, integratesPkgsTerraform
, path
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path integratesPkgs;
  makeSearchPaths = import (path "/makes/utils/make-search-paths") path integratesPkgs;
  terraformApply = import (path "/makes/utils/terraform-apply") path integratesPkgsTerraform;
in
makeEntrypoint rec {
  arguments = {
    envSearchPaths = makeSearchPaths [
      integratesPkgs.awscli
    ];
    envTerraformApply = "${terraformApply {
      inherit name;
      product = "integrates";
      target = "integrates/deploy/cluster/terraform";
    }}/bin/${name}";
    envUtilsAws = import (path "/makes/utils/aws") path integratesPkgs;
    envUtilsSops = import (path "/makes/utils/sops") path integratesPkgs;
  };
  name = "integrates-infra-cluster-apply";
  template = path "/makes/applications/integrates/infra/cluster/apply/entrypoint.sh";
}
