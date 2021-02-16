path: pkgs:

{ name
, product
, target
, secretsPath ? ""
, keys
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path pkgs;
  terraformApply = import (path "/makes/utils/terraform-apply") path pkgs;
  terraformTaint = import (path "/makes/utils/terraform-taint") path pkgs;
in
makeEntrypoint {
  arguments = {
    envTarget = target;
    envKeys = builtins.toJSON keys;
  };
  inherit name;
  searchPaths = {
    envPaths = [
      pkgs.curl
      pkgs.jq
      pkgs.terraform_0_13
      (terraformApply {
        name = "terraform-apply";
        inherit product;
        inherit target;
        inherit secretsPath;
      })
      (terraformTaint {
        name = "terraform-taint";
        inherit product;
        inherit target;
        inherit secretsPath;
      })
    ];
    envUtils = [
      "/makes/utils/gitlab"
    ];
  };
  template = path "/makes/utils/user-rotate-keys/entrypoint.sh";
}
