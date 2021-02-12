{ integratesPkgs
, makeEntrypoint
, path
, ...
} @ _:
makeEntrypoint integratesPkgs {
  arguments = {
    envManifests = path "/makes/applications/integrates/back/deploy/prod/k8s";
  };
  searchPaths = {
    envPaths = [
      integratesPkgs.awscli
      integratesPkgs.curl
      integratesPkgs.envsubst
      integratesPkgs.kubectl
      integratesPkgs.utillinux
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "integrates-back-deploy-prod";
  template = path "/makes/applications/integrates/back/deploy/prod/entrypoint.sh";
}
