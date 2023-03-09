{
  makeRubyGemsEnvironment,
  projectPath,
  ...
}:
makeRubyGemsEnvironment {
  name = "integrates-tools-asciidoctor-pdf";
  ruby = "2.7";
  sourcesYaml = projectPath "/integrates/back/tools/asciidoctor-pdf/sources.yaml";
}
