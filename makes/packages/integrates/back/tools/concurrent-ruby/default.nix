{ nixpkgs2
, path
, ...
}:
let
  buildRubyRequirement = import (path "/makes/utils/build-ruby-requirement") path nixpkgs2;
in
buildRubyRequirement {
  dependencies = [ ];
  name = "integrates-tools-concurrent-ruby";
  ruby = nixpkgs2.ruby_2_6;
  requirement = "concurrent-ruby:1.1.6";
}
