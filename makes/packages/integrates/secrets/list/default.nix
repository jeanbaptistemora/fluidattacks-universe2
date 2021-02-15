{ integratesPkgs
, makeTemplate
, path
, ...
} @ _:
makeTemplate integratesPkgs {
  name = "integrates-secrets-list";
  template = path "/makes/packages/integrates/secrets/list/template.sh";
}
