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
    envTerraformApply = "${terraformApply {
      inherit name;
      inherit product;
      inherit target;
      inherit secretsPath;
    }}/bin/${name}";
    envTerraformTaint = "${terraformTaint {
      inherit name;
      inherit product;
      inherit target;
      inherit secretsPath;
    }}/bin/${name}";
    envTarget = target;
    envKeys = builtins.toJSON keys;
  };
  inherit name;
  searchPaths = {
    envPaths = [
      pkgs.curl
      pkgs.jq
      pkgs.terraform_0_13
    ];
    envUtils = [
      "/makes/utils/gitlab"
    ];
  };
  template = path "/makes/utils/user-rotate-keys/entrypoint.sh";
}
