{ integratesPkgs
, path
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path integratesPkgs;
in
makeEntrypoint {
  arguments = {
    envExternalC3 = integratesPkgs.fetchzip {
      url = "https://github.com/c3js/c3/archive/v0.7.18.zip";
      sha256 = "Wqfm34pE2NDMu1JMwBAR/1jcZZlVBfxRKGp/YPNlocU=";
    };
    envUtilsAws = import (path "/makes/utils/aws") path integratesPkgs;
    envUtilsCommon = path "/makes/utils/common/template.sh";
  };
  name = "integrates-deploy-front";
  template = path "/makes/applications/integrates/deploy/front/entrypoint.sh";
}
