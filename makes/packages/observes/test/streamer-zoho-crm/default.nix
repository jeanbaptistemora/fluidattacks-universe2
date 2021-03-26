{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-test-streamer-zoho-crm";
  arguments = {
    envSrc = path "/observes/singer/streamer_zoho_crm";
    envTestDir = "tests";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.tester
      packages.observes.env.development.streamer-zoho-crm
    ];
  };
  builder = path "/makes/packages/observes/generic/tester/test_builder.sh";
}
