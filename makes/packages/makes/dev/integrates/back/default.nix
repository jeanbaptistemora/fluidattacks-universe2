{ makeTemplate
, packages
, path
, ...
}:
makeTemplate {
  arguments = {
    envIntegratesBackEnv = packages.integrates.back.env;
  };
  name = "makes-dev-integrates-back";
  template = path "/makes/packages/makes/dev/integrates/back/template.sh";
}
