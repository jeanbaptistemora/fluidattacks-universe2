{ nixpkgs2
, path
, ...
}:
let
  buildRubyRequirement = import (path "/makes/utils/build-ruby-requirement") path nixpkgs2;
in
buildRubyRequirement {
  dependencies = [
    nixpkgs2.gcc
    nixpkgs2.gnumake
    nixpkgs2.rake
  ];
  name = "integrates-mobile-tools-fastlane";
  ruby = nixpkgs2.ruby;
  requirement = "fastlane:2.172.0";
}
