{ makeTemplate
, packages
, path
, ...
}:
makeTemplate {
  arguments = {
    envToolsAsciidoctorPdf = packages.integrates.back.tools.asciidoctor-pdf;
    envToolsConcurrentRuby = packages.integrates.back.tools.concurrent-ruby;
  };
  name = "integrates-tools";
  searchPaths.envSources = [
    packages.integrates.back.tools.asciidoctor
    packages.integrates.back.tools.secure-spreadsheet
  ];
  template = path "/makes/packages/integrates/back/tools/template.sh";
}
