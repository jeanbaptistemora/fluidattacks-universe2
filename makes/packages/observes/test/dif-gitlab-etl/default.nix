{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-test-dif-gitlab-etl";
  arguments = {
    envSrc = path "/observes/etl/dif_gitlab_etl";
    envTestDir = "tests";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.tester
      packages.observes.env.gitlab-etl.development
    ];
  };
  builder = path "/makes/packages/observes/generic/tester/test_builder.sh";
}
