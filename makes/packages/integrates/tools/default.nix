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
    envToolsAsciidoctor = outputs.packages."integrates/tools/asciidoctor";
    envToolsAsciidoctorPdf = outputs.packages."integrates/tools/asciidoctor-pdf";
    envToolsConcurrentRuby = outputs.packages."integrates/tools/concurrent-ruby";
  };
  name = "integrates-tools";
  template = path "/makes/packages/integrates/tools/template.sh";
}
