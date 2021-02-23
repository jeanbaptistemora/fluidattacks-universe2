{ integratesMobilePkgs
, path
, ...
}:
let
  buildRubyRequirement = import (path "/makes/utils/build-ruby-requirement") path integratesMobilePkgs;
in
buildRubyRequirement {
  dependencies = [
    integratesMobilePkgs.gcc
    integratesMobilePkgs.gnumake
    integratesMobilePkgs.rake
  ];
  name = "integrates-mobile-tools-fastlane";
  ruby = integratesMobilePkgs.ruby;
  requirement = "fastlane:2.172.0";
}
