{ nixpkgs
, makeTemplate
, packages
, path
, ...
}:
makeTemplate {
  arguments = {
    envExternalC3 = nixpkgs.fetchzip {
      url = "https://github.com/c3js/c3/archive/v0.7.18.zip";
      sha256 = "Wqfm34pE2NDMu1JMwBAR/1jcZZlVBfxRKGp/YPNlocU=";
    };
    envSetupIntegratesFrontDevRuntime = packages.integrates.front.config.dev-runtime;
    envIntegratesBackAppTemplates = path "/integrates/back/app/templates/static";
    envIntegratesFront = path "/integrates/front";
    envJqueryCommentsPatch = path "/makes/packages/integrates/front/build-pkg/jquery-comments.diff";
  };
  template = path "/makes/packages/integrates/front/build-pkg/template.sh";
  name = "integrates-front-build-pkg";
  searchPaths = {
    envPaths = [
      nixpkgs.nodejs
      nixpkgs.patch
    ];
    envNodeBinaries = [
      packages.integrates.front.config.dev-runtime
    ];
  };
}
