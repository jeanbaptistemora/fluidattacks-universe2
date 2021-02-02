{ makesPkgs
, outputs
, path
, ...
} @ _:
let
  makeTemplate = import (path "/makes/utils/make-template") path makesPkgs;
in
makeTemplate {
  arguments = {
    envBaseSearchPaths = import (path "/makes/utils/make-search-paths") path makesPkgs [
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
    envSkimsSetupDevelopment = outputs.packages."skims/config-development";
    envSkimsSetupRuntime = outputs.packages."skims/config-runtime";
  };
  name = "makes-dev";
  template = path "/makes/packages/makes/dev/template.sh";
}
