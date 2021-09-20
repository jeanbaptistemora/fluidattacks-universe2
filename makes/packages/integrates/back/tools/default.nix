{ makeTemplate
, packages
, path
, ...
}:
makeTemplate {
  arguments = {
    envToolsConcurrentRuby = packages.integrates.back.tools.concurrent-ruby;
  };
  name = "integrates-tools";
  searchPaths.envSources = [
    packages.integrates.back.tools.asciidoctor-pdf
    packages.integrates.back.tools.secure-spreadsheet
  ];
  template = path "/makes/packages/integrates/back/tools/template.sh";
}
