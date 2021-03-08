{ buildRubyRequirement
, nixpkgs
, ...
}:
buildRubyRequirement {
  name = "integrates-tools-concurrent-ruby";
  ruby = nixpkgs.ruby_2_6;
  requirement = "concurrent-ruby:1.1.6";
}
