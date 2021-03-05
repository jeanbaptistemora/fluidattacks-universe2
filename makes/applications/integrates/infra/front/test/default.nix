{ nixpkgs2
, makeEntrypoint
, path
, terraformTest
, ...
}:
makeEntrypoint rec {
  arguments = {
    envUtilsAws = import (path "/makes/utils/aws") path nixpkgs2;
    envUtilsSops = import (path "/makes/utils/sops") path nixpkgs2;
    envTerraformTest = "${terraformTest {
      inherit name;
      product = "integrates";
      target = "integrates/deploy/front/terraform";
    }}/bin/${name}";
  };
  name = "integrates-infra-front-test";
  template = path "/makes/applications/integrates/infra/front/test/entrypoint.sh";
}
