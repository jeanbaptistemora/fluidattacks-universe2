{ buildRubyRequirement
, nixpkgs
, ...
}:
buildRubyRequirement {
  name = "integrates-tools-asciidoctor";
  ruby = nixpkgs.ruby_2_6;
  requirement = "asciidoctor:2.0.10";
}
