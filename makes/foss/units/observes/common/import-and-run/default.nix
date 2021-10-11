{ makeTemplate
, path
, ...
}:
makeTemplate {
  name = "observes-generic-runner";
  template = path "/makes/foss/units/observes/common/import-and-run/template.sh";
}
