{ nixpkgs
, makeEntrypoint
, path
, terraformApply
, ...
}:
makeEntrypoint rec {
  arguments = {
    envTerraformApply = "${terraformApply {
      inherit name;
      product = "integrates";
      target = "integrates/deploy/cluster/terraform";
    }}/bin/${name}";
    envUtilsAws = import (path "/makes/utils/aws") path nixpkgs;
    envUtilsSops = import (path "/makes/utils/sops") path nixpkgs;
  };
  name = "integrates-infra-cluster-apply";
  template = path "/makes/applications/integrates/infra/cluster/apply/entrypoint.sh";
}
