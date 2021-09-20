{ makes
, packages
, ...
}:
makes.makeSearchPaths {
  source = [
    packages.integrates.back.tools.asciidoctor-pdf
    packages.integrates.back.tools.concurrent-ruby
    packages.integrates.back.tools.secure-spreadsheet
  ];
}
