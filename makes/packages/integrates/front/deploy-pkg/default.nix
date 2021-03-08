{ nixpkgs
, makeTemplate
, packages
, path
, ...
}:
makeTemplate {
  name = "integrates-front-deploy-pkg";
  searchPaths = {
    envPaths = [
      nixpkgs.findutils
      nixpkgs.gnused
      packages.makes.announce.bugsnag
    ];
    envUtils = [
      "/makes/utils/aws"
    ];
  };
  template = path "/makes/packages/integrates/front/deploy-pkg/template.sh";
}
