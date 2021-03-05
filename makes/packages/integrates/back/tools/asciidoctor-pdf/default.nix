{ buildRubyRequirement
, nixpkgs
, ...
}:
buildRubyRequirement {
  dependencies = [ ];
  name = "integrates-tools-asciidoctor-pdf";
  ruby = nixpkgs.ruby_2_6;
  requirement = "asciidoctor-pdf:1.5.0.rc.3";
}
