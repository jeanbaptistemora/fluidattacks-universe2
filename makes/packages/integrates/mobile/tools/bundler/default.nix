{ buildRubyRequirement
, nixpkgs
, ...
}:
buildRubyRequirement {
  dependencies = [ ];
  name = "integrates-mobile-tools-bundler";
  ruby = nixpkgs.ruby;
  requirement = "bundler:2.2.6";
}
