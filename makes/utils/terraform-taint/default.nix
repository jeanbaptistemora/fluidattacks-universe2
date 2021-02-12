path: pkgs:

{ name
, product
, target
, secrets_path ? ""
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path pkgs;
in
makeEntrypoint {
  arguments = {
    envProduct = product;
    envTarget = target;
    envSecretsPath = secrets_path;
    envUtilsCloudflare = import (path "/makes/utils/cloudflare") path pkgs;
    envUtilsAws = import (path "/makes/utils/aws") path pkgs;
  };
  inherit name;
  searchPaths = {
    envPaths = [
      pkgs.awscli
      pkgs.git
      pkgs.terraform_0_13
    ];
  };
  template = path "/makes/utils/terraform-taint/entrypoint.sh";
}
