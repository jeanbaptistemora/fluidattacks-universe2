{ inputs
, libGit
, makeTemplate
, outputs
, projectPath
, ...
}:
makeTemplate {
  name = "integrates-front-deploy";
  replace = {
    __argCompiledFront__ = outputs."/integrates/front/build";
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.findutils
      inputs.nixpkgs.gnused
      outputs."/makes/announce/bugsnag"
    ];
    source = [
      libGit
      (outputs."/utils/aws")
      (inputs.legacy.importUtility "cloudflare")
      (outputs."/utils/sops")
    ];
  };
  template = projectPath "/makes/foss/units/integrates/front/deploy/template.sh";
}
