{ integratesPkgs
, integratesPkgsTerraform
, path
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path integratesPkgs;
  makeSearchPaths = import (path "/makes/utils/make-search-paths") path integratesPkgs;
  terraformTest = import (path "/makes/utils/terraform-test") path integratesPkgsTerraform;
in
makeEntrypoint rec {
  arguments = {
    envSearchPaths = makeSearchPaths [
      integratesPkgs.awscli
    ];
    envUtilsAws = import (path "/makes/utils/aws") path integratesPkgs;
    envUtilsSops = import (path "/makes/utils/sops") path integratesPkgs;
    envTerraformTest = "${terraformTest {
      inherit name;
      product = "integrates";
      target = "integrates/deploy/cluster/terraform";
    }}/bin/${name}";
  };
  name = "integrates-infra-cluster-test";
  template = path "/makes/applications/integrates/infra-cluster-test/entrypoint.sh";
}
