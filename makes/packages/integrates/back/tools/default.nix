{ integratesPkgs
, packages
, path
, ...
}:
let
  makeTemplate = import (path "/makes/utils/make-template") path integratesPkgs;
in
makeTemplate {
  arguments = {
    envToolsAsciidoctor = packages.integrates.back.tools.asciidoctor;
    envToolsAsciidoctorPdf = packages.integrates.back.tools.asciidoctor-pdf;
    envToolsConcurrentRuby = packages.integrates.back.tools.concurrent-ruby;
    envToolsSecureSpreadsheet = packages.integrates.back.tools.secure-spreadsheet;
  };
  name = "integrates-tools";
  template = path "/makes/packages/integrates/back/tools/template.sh";
}
