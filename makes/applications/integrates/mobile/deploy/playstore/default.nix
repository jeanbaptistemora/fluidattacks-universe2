{ integratesMobilePkgs
, makeEntrypoint
, packages
, path
, ...
} @ _:
makeEntrypoint integratesMobilePkgs {
  arguments = {
    envSecretsProd = path "/integrates/secrets-production.yaml";
  };
  name = "integrates-mobile-deploy-playstore";
  searchPaths = {
    envPaths = [
      integratesMobilePkgs.git
      integratesMobilePkgs.nodejs-12_x
      integratesMobilePkgs.ruby
    ];
    envSources = [
      packages.integrates.mobile.tools
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/git"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/integrates/mobile/deploy/playstore/entrypoint.sh";
}
