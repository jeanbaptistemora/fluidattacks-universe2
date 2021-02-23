{ integratesPkgs
, path
, ...
}:
let
  buildRubyRequirement = import (path "/makes/utils/build-ruby-requirement") path integratesPkgs;
in
buildRubyRequirement {
  dependencies = [ ];
  name = "integrates-tools-asciidoctor";
  ruby = integratesPkgs.ruby_2_6;
  requirement = "asciidoctor:2.0.10";
}
