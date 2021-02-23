{ integratesPkgs
, path
, ...
}:
let
  buildRubyRequirement = import (path "/makes/utils/build-ruby-requirement") path integratesPkgs;
in
buildRubyRequirement {
  dependencies = [ ];
  name = "integrates-tools-concurrent-ruby";
  ruby = integratesPkgs.ruby_2_6;
  requirement = "concurrent-ruby:1.1.6";
}
