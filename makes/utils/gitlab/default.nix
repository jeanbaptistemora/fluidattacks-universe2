path: pkgs:
let
  makeSearchPaths = import (path "/makes/utils/make-search-paths") path pkgs;
  makeTemplate = import (path "/makes/utils/make-template") path pkgs;
in
makeTemplate {
  arguments = {
    envSearchPaths = makeSearchPaths [
      pkgs.cacert
      pkgs.curl
    ];
  };
  name = "utils-gitlab";
  template = path "/makes/utils/gitlab/entrypoint.sh";
}
