{ makeTemplate
, ...
}:
makeTemplate {
  name = "observes-generic-runner";
  template = ./template.sh;
}
