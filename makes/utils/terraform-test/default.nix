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
    envTflint = "${pkgs.tflint}/bin/tflint";
    envTflintConfig = path "/.tflint.hcl";
    envUtilsBashLibAws = import (path "/makes/utils/aws") path pkgs;
  };
  inherit name;
  template = path "/makes/utils/terraform-test/entrypoint.sh";
}
