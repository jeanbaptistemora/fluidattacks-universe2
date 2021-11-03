{ inputs
, makeScript
, outputs
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
      (outputs."/utils/aws")
    ];
  };
  name = "integrates-back-deploy-dev";
  entrypoint = projectPath "/makes/foss/units/integrates/back/deploy/dev/entrypoint.sh";
}
