{ integratesPkgs
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
      integratesPkgs.awscli
      integratesPkgs.envsubst
      integratesPkgs.kubectl
      integratesPkgs.utillinux
    ];
    envUtils = [
      "/makes/utils/aws"
    ];
  };
  name = "integrates-back-deploy-dev";
  template = path "/makes/applications/integrates/back/deploy/dev/entrypoint.sh";
}
