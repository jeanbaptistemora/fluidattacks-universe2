{ terraformTest
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint rec {
  name = "forces-infra-test";
  searchPaths = {
    envPaths = [
      (terraformTest {
        name = "terraform-test";
        product = "forces";
        target = "forces/infra";
      })
    ];
    envSources = [ packages.melts.lib ];
  };
  template = path "/makes/applications/forces/infra-test/entrypoint.sh";
}
