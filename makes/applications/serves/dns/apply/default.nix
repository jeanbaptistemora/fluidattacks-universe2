{ servesPkgs
, servesPkgsTerraform
, path
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path servesPkgs;
  terraformApply = import (path "/makes/utils/terraform-apply") path servesPkgsTerraform;
in
makeEntrypoint rec {
  arguments = {
    envUtilsAws = import (path "/makes/utils/aws") path servesPkgs;
    envUtilsSops = import (path "/makes/utils/sops") path servesPkgs;
    envTerraformApply = "${terraformApply {
      inherit name;
      product = "serves";
      target = "serves/dns/terraform";
    }}/bin/${name}";
  };
  name = "serves-dns-apply";
  template = path "/makes/applications/serves/dns/apply/entrypoint.sh";
}
