path: pkgs:

{ name
, product
, target
, secrets_path ? ""
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path pkgs;
  makeSearchPaths = import (path "/makes/utils/make-search-paths") path pkgs;
in
makeEntrypoint {
  arguments = {
    envSearchPaths = makeSearchPaths [
      pkgs.terraform_0_13
    ];
    envProduct = product;
    envTarget = target;
    envSecretsPath = secrets_path;
    envUtilsCloudflare = import (path "/makes/utils/cloudflare") path pkgs;
    envUtilsAws = import (path "/makes/utils/aws") path pkgs;
  };
  inherit name;
  template = path "/makes/utils/terraform-apply/entrypoint.sh";
}
