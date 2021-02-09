{ integratesPkgs
, path
, ...
} @ attrs:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path integratesPkgs;
  makeSearchPaths = import (path "/makes/utils/make-search-paths") path integratesPkgs;
in
makeEntrypoint {
  arguments = {
    envSearchPaths = makeSearchPaths [
      integratesPkgs.findutils
      integratesPkgs.iproute
      integratesPkgs.nodejs-12_x
      integratesPkgs.xdg_utils
    ];
    envSecretsDev = path "/integrates/secrets-development.yaml";
    envSetupIntegratesMobileDevRuntime = import (path "/makes/packages/integrates/mobile/config/dev-runtime") attrs.copy;
    envUtilsAws = import (path "/makes/utils/aws") path integratesPkgs;
    envUtilsCommon = path "/makes/utils/common/template.sh";
    envUtilsSops = import (path "/makes/utils/sops") path integratesPkgs;
  };
  name = "integrates-mobile";
  template = path "/makes/applications/integrates/mobile/entrypoint.sh";
}
