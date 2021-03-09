{ makeTemplate
, path
, ...
}:
makeTemplate {
  name = "observes-generic-tester";
  template = path "/makes/packages/observes/generic/tester/template.sh";
}
