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
      makesPkgs.awscli2
      makesPkgs.cloc
      makesPkgs.nixpkgs-fmt
      makesPkgs.sops
      makesPkgs.terraform
      makesPkgs.tokei
    ];
    envSkimsSetupDevelopment = outputs.packages.skims-config-setup-skims-development;
    envSkimsSetupRuntime = outputs.packages.skims-config-setup-skims-runtime;
  };
  name = "makes-dev";
  template = path "/makes/makes/dev/template.sh";
}
