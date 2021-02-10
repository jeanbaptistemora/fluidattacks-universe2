path: pkgs:

{ name
, product
, target
, secrets_path ? ""
, resources_to_taint
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
    ];
    envProduct = product;
    envTarget = target;
    envSecretsPath = secrets_path;
    envResourcesToTaint = pkgs.lib.strings.escapeShellArgs resources_to_taint;
    envUtilsCloudflare = import (path "/makes/utils/cloudflare") path pkgs;
    envUtilsAws = import (path "/makes/utils/aws") path pkgs;
  };
  inherit name;
  template = path "/makes/utils/terraform-taint/entrypoint.sh";
}
