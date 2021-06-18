path: pkgs:

{ name
, product
, target
, secretsPath ? null
, vars ? [ ]
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path pkgs;
in
makeEntrypoint {
  arguments = {
    envProduct = product;
    envTarget = target;
    envSecretsPath = if secretsPath == null then "" else path "/${secretsPath}";
    envVars = vars;
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
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/utils/terraform-taint/entrypoint.sh";
}
