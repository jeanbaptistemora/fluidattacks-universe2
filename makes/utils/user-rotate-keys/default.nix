path: pkgs:

{ name
, product
, target
, secrets_path ? ""
, gitlab_project_id
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
      inherit secrets_path;
    }}/bin/${name}";
    envTerraformTaint = "${terraformTaint {
      inherit name;
      inherit product;
      inherit target;
      inherit secrets_path;
    }}/bin/${name}";
    envTarget = target;
    envGitlabProjectId = gitlab_project_id;
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
