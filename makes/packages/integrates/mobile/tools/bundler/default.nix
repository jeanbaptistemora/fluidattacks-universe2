{ nixpkgs2
, path
, ...
}:
let
  buildRubyRequirement = import (path "/makes/utils/build-ruby-requirement") path nixpkgs2;
in
buildRubyRequirement {
  dependencies = [ ];
  name = "integrates-mobile-tools-bundler";
  ruby = nixpkgs2.ruby;
  requirement = "bundler:2.2.6";
}
