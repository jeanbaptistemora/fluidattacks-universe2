path: pkgs:

{ name
, product
, target
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path pkgs;
in
makeEntrypoint {
  arguments = {
    envProduct = product;
    envTarget = target;
    envTerraform = "${pkgs.terraform_0_13}/bin/terraform";
    envUtilsBashLibAws = import (path "/makes/utils/bash-lib/aws") path pkgs;
  };
  location = "/bin/${name}";
  inherit name;
  template = path "/makes/utils/bash-lib/terraform-apply/entrypoint.sh";
}
