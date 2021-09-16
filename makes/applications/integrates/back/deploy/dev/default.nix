{ nixpkgs
, makeEntrypoint
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envManifests = path "/makes/applications/integrates/back/deploy/dev/k8s";
  };
  searchPaths = {
    envPaths = [
      nixpkgs.awscli
      nixpkgs.envsubst
      nixpkgs.kubectl
      nixpkgs.utillinux
      nixpkgs.yq
    ];
    envUtils = [
      "/makes/utils/aws"
    ];
  };
  name = "integrates-back-deploy-dev";
  template = path "/makes/applications/integrates/back/deploy/dev/entrypoint.sh";
}
