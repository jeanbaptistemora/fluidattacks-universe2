{ inputs
, libGit
, makeTemplate
, outputs
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
      (outputs."/utils/cloudflare")
      (outputs."/utils/sops")
    ];
  };
  template = ./template.sh;
}
