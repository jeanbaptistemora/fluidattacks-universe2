{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-lint-target-redshift";
  arguments = {
    envSrc = path "/observes/singer/target_redshift";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.linter
      packages.observes.env.target-redshift.runtime
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/lint_builder.sh";
}
