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
  };
  inherit name;
  searchPaths = {
    envPaths = [
      pkgs.awscli
      pkgs.git
      pkgs.terraform_0_13
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/cloudflare"
    ];
  };
  template = path "/makes/utils/terraform-taint/entrypoint.sh";
}
