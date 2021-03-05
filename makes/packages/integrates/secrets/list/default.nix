{ makeTemplate
, path
, ...
}:
makeTemplate {
  name = "integrates-secrets-list";
  template = path "/makes/packages/integrates/secrets/list/template.sh";
}
