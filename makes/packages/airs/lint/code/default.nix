{ airsPkgs
, makeDerivation
, packages
, path
, ...
}:
makeDerivation airsPkgs {
  arguments = {
    envLintConfig = path "/integrates/front";
    envAirsNewFront = path "/airs/new-front";
    envAirsNpm = packages.airs.npm;
  };
  builder = path "/makes/packages/airs/lint/code/builder.sh";
  name = "airs-lint-code";
}
