{ nixpkgs
, makeEntrypoint
, path
, terraformApply
, ...
}:
makeEntrypoint rec {
  arguments = {
    envUtilsAws = import (path "/makes/utils/aws") path nixpkgs;
    envUtilsSops = import (path "/makes/utils/sops") path nixpkgs;
    envTerraformApply = "${terraformApply {
      inherit name;
      product = "integrates";
      target = "integrates/deploy/front/terraform";
    }}/bin/${name}";
  };
  name = "integrates-infra-front-apply";
  template = path "/makes/applications/integrates/infra/front/apply/entrypoint.sh";
}
