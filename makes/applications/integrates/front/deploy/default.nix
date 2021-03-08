{ nixpkgs
, makeTemplate
, packages
, path
, ...
}:
makeTemplate {
  name = "integrates-front-deploy";
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
  template = path "/makes/applications/integrates/front/deploy/template.sh";
}
