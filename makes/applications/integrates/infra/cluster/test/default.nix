{ integratesPkgs
, makeEntrypoint
, path
, terraformTest
, ...
}:
makeEntrypoint rec {
  arguments = {
    envUtilsAws = import (path "/makes/utils/aws") path integratesPkgs;
    envUtilsSops = import (path "/makes/utils/sops") path integratesPkgs;
    envTerraformTest = "${terraformTest {
      inherit name;
      product = "integrates";
      target = "integrates/deploy/cluster/terraform";
    }}/bin/${name}";
  };
  name = "integrates-infra-cluster-test";
  template = path "/makes/applications/integrates/infra/cluster/test/entrypoint.sh";
}
