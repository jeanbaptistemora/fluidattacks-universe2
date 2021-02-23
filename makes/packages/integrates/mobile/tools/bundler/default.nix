{ integratesMobilePkgs
, path
, ...
}:
let
  buildRubyRequirement = import (path "/makes/utils/build-ruby-requirement") path integratesMobilePkgs;
in
buildRubyRequirement {
  dependencies = [ ];
  name = "integrates-mobile-tools-bundler";
  ruby = integratesMobilePkgs.ruby;
  requirement = "bundler:2.2.6";
}
