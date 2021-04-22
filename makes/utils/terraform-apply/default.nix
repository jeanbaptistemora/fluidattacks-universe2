path: pkgs:

{ name
, product
, target
, secretsPath ? ""
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path pkgs;
in
makeEntrypoint {
  arguments = {
    envProduct = product;
    envTarget = target;
    envSecretsPath =
      if secretsPath != "" then path "/${secretsPath}" else secretsPath;
  };
  inherit name;
  searchPaths = {
    envPaths = [
      pkgs.awscli
      pkgs.git
      pkgs.kubectl
      pkgs.terraform_0_13
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/utils/terraform-apply/entrypoint.sh";
}
