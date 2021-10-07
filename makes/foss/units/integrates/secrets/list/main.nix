{ makeTemplate
, projectPath
, ...
}:
makeTemplate {
  name = "integrates-secrets-list";
  template = projectPath "/makes/foss/units/integrates/secrets/list/template.sh";
}
