path: pkgs:

{ name
, product
, target
, secrets_path ? ""
, gitlab_project_id
, keys
,
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path pkgs;
  makeSearchPaths = import (path "/makes/utils/make-search-paths") path pkgs;
  terraformTaint = import (path "/makes/utils/terraform-taint") path pkgs;
in
makeEntrypoint {
  arguments = {
    envSearchPaths = makeSearchPaths [
      pkgs.cacert
      pkgs.curl
      pkgs.jq
      pkgs.terraform_0_13
    ];
    envTerraformTaint = "${terraformTaint {
      inherit name;
      inherit product;
      inherit target;
      inherit secrets_path;
    }}/bin/${name}";
    envUtilsGitlab = import (path "/makes/utils/gitlab") path pkgs;
    envTarget = target;
    envGitlabProjectId = gitlab_project_id;
    envKeys = builtins.toJSON keys;
  };
  inherit name;
  template = path "/makes/packages/serves/users-rotate-keys/entrypoint.sh";
}
