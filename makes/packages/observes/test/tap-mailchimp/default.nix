{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-lint-tap-mailchimp";
  arguments = {
    envSrc = path "/observes/singer/tap_mailchimp";
    envTestDir = "tests";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.tester
      packages.observes.env.tap-mailchimp.development
    ];
  };
  builder = path "/makes/packages/observes/generic/tester/test_builder.sh";
}
