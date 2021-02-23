{ integratesPkgs
, path
, ...
}:
let
  buildRubyRequirement = import (path "/makes/utils/build-ruby-requirement") path integratesPkgs;
in
buildRubyRequirement {
  dependencies = [ ];
  name = "integrates-tools-asciidoctor-pdf";
  ruby = integratesPkgs.ruby_2_6;
  requirement = "asciidoctor-pdf:1.5.0.rc.3";
}
