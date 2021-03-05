{ integratesPkgs
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envFirefox = integratesPkgs.firefox;
    envGeckodriver = integratesPkgs.geckodriver;
  };
  searchPaths = {
    envPaths = [
      integratesPkgs.kubectl
      packages.integrates.web.e2e.pypi
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "integrates-web-e2e";
  template = path "/makes/applications/integrates/web/e2e/entrypoint.sh";
}
