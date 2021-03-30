{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-lint-target-redshift";
  arguments = {
    envSrc = path "/observes/singer/target_redshift_2";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.linter
      packages.observes.env.target-redshift.development
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/lint_builder.sh";
}
