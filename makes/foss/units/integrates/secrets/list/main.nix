{ makeTemplate
, ...
}:
makeTemplate {
  name = "integrates-secrets-list";
  template = ./template.sh;
}
