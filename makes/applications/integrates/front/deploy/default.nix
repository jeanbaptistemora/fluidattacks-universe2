{ integratesPkgs
, makeEntrypoint
, path
, ...
}:
makeEntrypoint integratesPkgs {
  arguments = {
    envExternalC3 = integratesPkgs.fetchzip {
      url = "https://github.com/c3js/c3/archive/v0.7.18.zip";
      sha256 = "Wqfm34pE2NDMu1JMwBAR/1jcZZlVBfxRKGp/YPNlocU=";
    };
  };
  name = "integrates-front-deploy";
  searchPaths = {
    envUtils = [
      "/makes/utils/aws"
    ];
  };
  template = path "/makes/applications/integrates/front/deploy/entrypoint.sh";
}
