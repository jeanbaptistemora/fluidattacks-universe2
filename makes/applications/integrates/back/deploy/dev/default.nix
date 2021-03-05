{ nixpkgs2
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
      nixpkgs2.awscli
      nixpkgs2.envsubst
      nixpkgs2.kubectl
      nixpkgs2.utillinux
    ];
    envUtils = [
      "/makes/utils/aws"
    ];
  };
  name = "integrates-back-deploy-dev";
  template = path "/makes/applications/integrates/back/deploy/dev/entrypoint.sh";
}
