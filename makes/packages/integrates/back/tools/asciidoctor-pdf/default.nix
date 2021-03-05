{ nixpkgs2
, path
, ...
}:
let
  buildRubyRequirement = import (path "/makes/utils/build-ruby-requirement") path nixpkgs2;
in
buildRubyRequirement {
  dependencies = [ ];
  name = "integrates-tools-asciidoctor-pdf";
  ruby = nixpkgs2.ruby_2_6;
  requirement = "asciidoctor-pdf:1.5.0.rc.3";
}
