{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-lint-singer-io";
  arguments = {
    envSrc = path "/observes/singer/streamer_gitlab";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.linter
      packages.observes.env.streamer-gitlab.development
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/lint_builder.sh";
}
