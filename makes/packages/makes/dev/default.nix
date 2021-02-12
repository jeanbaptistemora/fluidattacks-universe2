{ makesPkgs
, packages
, path
, ...
} @ _:
let
  makeTemplate = import (path "/makes/utils/make-template") path makesPkgs;
in
makeTemplate {
  arguments = {
    envBaseSearchPaths = import (path "/makes/utils/make-search-paths-deprecated") path makesPkgs [
      makesPkgs.awscli
      makesPkgs.cloc
      makesPkgs.jq
      makesPkgs.nixpkgs-fmt
      makesPkgs.redis
      makesPkgs.sops
      makesPkgs.terraform
      makesPkgs.tokei
      makesPkgs.yq
    ];
    envSkimsSetupDevelopment = packages."skims/config-development";
    envSkimsSetupRuntime = packages."skims/config-runtime";
  };
  name = "makes-dev";
  template = path "/makes/packages/makes/dev/template.sh";
}
