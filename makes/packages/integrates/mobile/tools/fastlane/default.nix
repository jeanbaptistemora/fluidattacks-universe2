{ buildRubyRequirement
, nixpkgs
, ...
}:
buildRubyRequirement {
  dependencies = [
    nixpkgs.gcc
    nixpkgs.gnumake
    nixpkgs.rake
  ];
  name = "integrates-mobile-tools-fastlane";
  ruby = nixpkgs.ruby;
  requirement = "fastlane:2.172.0";
}
