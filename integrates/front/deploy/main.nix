{
  inputs,
  libGit,
  makeTemplate,
  outputs,
  ...
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
      outputs."/common/announce/bugsnag"
    ];
    source = [
      libGit
      outputs."/common/utils/aws"
      outputs."/common/utils/cloudflare"
      outputs."/common/utils/sops"
    ];
  };
  template = ./template.sh;
}
