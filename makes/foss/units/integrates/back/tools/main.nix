{ makeSearchPaths
, outputs
, ...
}:
makeSearchPaths {
  source = [
    outputs."/integrates/back/tools/asciidoctor-pdf"
    outputs."/integrates/back/tools/concurrent-ruby"
    outputs."/integrates/back/tools/secure-spreadsheet"
  ];
}
