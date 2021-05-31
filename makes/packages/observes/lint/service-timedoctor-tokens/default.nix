{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-lint-service-timedoctor-tokens";
  arguments = {
    envSrc = path "/observes/services/timedoctor_tokens";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.linter
      packages.observes.env.service-timedoctor-tokens.runtime
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/lint_builder.sh";
}
