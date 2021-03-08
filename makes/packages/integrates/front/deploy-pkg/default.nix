{ makeTemplate
, path
, ...
}:
makeTemplate {
  name = "integrates-front-deploy-pkg";
  searchPaths = {
    envUtils = [
      "/makes/utils/aws"
    ];
  };
  template = path "/makes/packages/integrates/front/deploy-pkg/template.sh";
}
