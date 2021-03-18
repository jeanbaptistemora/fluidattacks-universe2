{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-lint-tap-mailchimp";
  arguments = {
    envSrc = path "/observes/singer/tap_mailchimp";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.linter
      packages.observes.env.development.tap-mailchimp
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/lint_builder.sh";
}
