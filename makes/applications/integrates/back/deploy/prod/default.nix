{ nixpkgs2
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
      nixpkgs2.awscli
      nixpkgs2.curl
      nixpkgs2.envsubst
      nixpkgs2.kubectl
      nixpkgs2.utillinux
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "integrates-back-deploy-prod";
  template = path "/makes/applications/integrates/back/deploy/prod/entrypoint.sh";
}
