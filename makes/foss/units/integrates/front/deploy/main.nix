{ inputs
, libGit
, makeTemplate
, projectPath
, ...
}:
makeTemplate {
  name = "integrates-front-deploy";
  replace = {
    __argCompiledFront__ = inputs.product.integrates-front-build;
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.findutils
      inputs.nixpkgs.gnused
      inputs.product.makes-announce-bugsnag
    ];
    source = [
      libGit
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "cloudflare")
      (inputs.legacy.importUtility "sops")
    ];
  };
  template = projectPath "/makes/foss/units/integrates/front/deploy/template.sh";
}
