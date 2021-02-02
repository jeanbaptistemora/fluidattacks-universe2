path: pkgs:

{ name
, product
, target
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path pkgs;
  makeSearchPaths = import (path "/makes/utils/make-search-paths") path pkgs;
in
makeEntrypoint {
  arguments = {
    envSearchPaths = makeSearchPaths [
      pkgs.awscli
      pkgs.git
      pkgs.terraform_0_13
      pkgs.tflint
    ];
    envProduct = product;
    envTarget = target;
    envTflintConfig = path "/.tflint.hcl";
    envUtilsBashLibAws = import (path "/makes/utils/aws") path pkgs;
  };
  inherit name;
  template = path "/makes/utils/terraform-test/entrypoint.sh";
}
