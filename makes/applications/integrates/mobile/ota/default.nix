{ integratesPkgs
, path
, ...
} @ attrs:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path integratesPkgs;
  makeSearchPaths = import (path "/makes/utils/make-search-paths-deprecated") path integratesPkgs;
in
makeEntrypoint {
  arguments = {
    envSearchPaths = makeSearchPaths [
      integratesPkgs.findutils
      integratesPkgs.gnused
      integratesPkgs.nodejs-12_x
    ];
    envSecretsDev = path "/integrates/secrets-development.yaml";
    envSecretsProd = path "/integrates/secrets-production.yaml";
    envSetupIntegratesMobileDevRuntime = import (path "/makes/packages/integrates/mobile/config/dev-runtime") attrs.copy;
    envUtilsAws = import (path "/makes/utils/aws") path integratesPkgs;
    envUtilsSops = import (path "/makes/utils/sops") path integratesPkgs;
  };
  name = "integrates-mobile-ota";
  template = path "/makes/applications/integrates/mobile/ota/entrypoint.sh";
}
