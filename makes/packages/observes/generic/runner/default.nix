{ makeTemplate
, path
, ...
}:
makeTemplate {
  name = "observes-generic-runner";
  template = path "/makes/packages/observes/generic/runner/template.sh";
}
