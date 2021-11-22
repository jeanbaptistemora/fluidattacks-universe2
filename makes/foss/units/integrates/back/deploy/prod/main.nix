{ inputs
, makeScript
, outputs
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
      (outputs."/utils/aws")
      (outputs."/utils/sops")
    ];
  };
  name = "integrates-back-deploy-prod";
  entrypoint = ./entrypoint.sh;
}
