{ nixpkgs2
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envFirefox = nixpkgs2.firefox;
    envGeckodriver = nixpkgs2.geckodriver;
  };
  searchPaths = {
    envPaths = [
      nixpkgs2.kubectl
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
