{ nixpkgs
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envFirefox = nixpkgs.firefox;
    envGeckodriver = nixpkgs.geckodriver;
  };
  searchPaths = {
    envPaths = [
      nixpkgs.kubectl
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
