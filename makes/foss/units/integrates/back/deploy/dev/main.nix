{ inputs
, makeScript
, projectPath
, ...
}:
makeScript {
  replace = {
    __argManifests__ = projectPath "/makes/foss/units/integrates/back/deploy/dev/k8s";
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.awscli
      inputs.nixpkgs.envsubst
      inputs.nixpkgs.kubectl
      inputs.nixpkgs.utillinux
      inputs.nixpkgs.yq
    ];
    source = [
      (inputs.legacy.importUtility "aws")
    ];
  };
  name = "integrates-back-deploy-dev";
  entrypoint = projectPath "/makes/foss/units/integrates/back/deploy/dev/entrypoint.sh";
}
