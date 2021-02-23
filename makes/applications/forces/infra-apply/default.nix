{ forcesPkgs
, forcesPkgsTerraform
, packages
, path
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path forcesPkgs;
  terraformApply = import (path "/makes/utils/terraform-apply") path forcesPkgsTerraform;
in
makeEntrypoint rec {
  arguments = {
    envTerraformApply = "${terraformApply {
      inherit name;
      product = "forces";
      target = "forces/infra";
    }}/bin/${name}";
    envUtilsMeltsLibCommon = packages.melts.lib;
  };
  name = "forces-infra-apply";
  template = path "/makes/applications/forces/infra-apply/entrypoint.sh";
}
