{ packages
, path
, integratesPkgs
, integratesPkgsTerraform
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path integratesPkgs;
  terraformApply = import (path "/makes/utils/terraform-apply") path integratesPkgsTerraform;
in
makeEntrypoint rec {
  arguments = {
    envTerraformApply = "${terraformApply {
      inherit name;
      product = "integrates";
      target = "integrates/deploy/secret-management/terraform";
    }}/bin/${name}";
    envUtilsMeltsLibCommon = packages.melts.lib;
  };
  name = "integrates-infra-secret-management-apply";
  template = path "/makes/applications/integrates/infra/secret-management/apply/entrypoint.sh";
}
