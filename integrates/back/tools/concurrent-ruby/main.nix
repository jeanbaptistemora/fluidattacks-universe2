{
  makeRubyGemsEnvironment,
  projectPath,
  ...
}:
makeRubyGemsEnvironment {
  name = "integrates-tools-concurrent-ruby";
  ruby = "2.7";
  sourcesYaml = projectPath "/integrates/back/tools/concurrent-ruby/sources.yaml";
}
