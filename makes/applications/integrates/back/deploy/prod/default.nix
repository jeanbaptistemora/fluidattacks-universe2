{ nixpkgs
, makeEntrypoint
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envManifests = path "/makes/applications/integrates/back/deploy/prod/k8s";
  };
  searchPaths = {
    envPaths = [
      nixpkgs.awscli
      nixpkgs.curl
      nixpkgs.envsubst
      nixpkgs.kubectl
      nixpkgs.utillinux
      nixpkgs.yq
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "integrates-back-deploy-prod";
  template = path "/makes/applications/integrates/back/deploy/prod/entrypoint.sh";
}
