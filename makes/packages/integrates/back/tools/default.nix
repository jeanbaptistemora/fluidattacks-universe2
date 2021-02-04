{ integratesPkgs
, outputs
, path
, ...
} @ _:
let
  makeTemplate = import (path "/makes/utils/make-template") path integratesPkgs;
in
makeTemplate {
  arguments = {
    envToolsAsciidoctor = outputs.packages."integrates/back/tools/asciidoctor";
    envToolsAsciidoctorPdf = outputs.packages."integrates/back/tools/asciidoctor-pdf";
    envToolsConcurrentRuby = outputs.packages."integrates/back/tools/concurrent-ruby";
    envToolsSecureSpreadsheet = outputs.packages."integrates/back/tools/secure-spreadsheet";
  };
  name = "integrates-tools";
  template = path "/makes/packages/integrates/back/tools/template.sh";
}
