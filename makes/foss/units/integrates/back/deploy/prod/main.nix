{ inputs
, makeScript
, projectPath
, ...
}:
makeScript {
  replace = {
    __argManifests__ = projectPath "/makes/foss/units/integrates/back/deploy/prod/k8s";
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.awscli
      inputs.nixpkgs.curl
      inputs.nixpkgs.envsubst
      inputs.nixpkgs.kubectl
      inputs.nixpkgs.utillinux
      inputs.nixpkgs.yq
    ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "integrates-back-deploy-prod";
  entrypoint = projectPath "/makes/foss/units/integrates/back/deploy/prod/entrypoint.sh";
}
