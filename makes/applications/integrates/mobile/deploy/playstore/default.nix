{ nixpkgs
, makeEntrypoint
, packages
, path
, ...
} @ _:
makeEntrypoint {
  arguments = {
    envSecretsProd = path "/integrates/secrets-production.yaml";
  };
  name = "integrates-mobile-deploy-playstore";
  searchPaths = {
    envPaths = [
      nixpkgs.git
      nixpkgs.nodejs-12_x
      nixpkgs.ruby
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
