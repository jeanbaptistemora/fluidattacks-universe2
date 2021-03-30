{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-test-target-redshift";
  arguments = {
    envSrc = path "/observes/singer/target_redshift_2";
    envTestDir = "tests";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.tester
      packages.observes.env.target-redshift.development
    ];
  };
  builder = path "/makes/packages/observes/generic/tester/test_builder.sh";
}
