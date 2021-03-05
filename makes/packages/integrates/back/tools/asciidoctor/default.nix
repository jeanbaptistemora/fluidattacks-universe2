{ nixpkgs2
, path
, ...
}:
let
  buildRubyRequirement = import (path "/makes/utils/build-ruby-requirement") path nixpkgs2;
in
buildRubyRequirement {
  dependencies = [ ];
  name = "integrates-tools-asciidoctor";
  ruby = nixpkgs2.ruby_2_6;
  requirement = "asciidoctor:2.0.10";
}
