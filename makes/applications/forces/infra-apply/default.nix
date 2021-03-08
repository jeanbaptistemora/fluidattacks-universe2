{ makeEntrypoint
, packages
, path
, terraformApply
, ...
}:
makeEntrypoint {
  name = "forces-infra-apply";
  searchPaths = {
    envPaths = [
      (terraformApply {
        name = "terraforma-apply";
        product = "forces";
        target = "forces/infra";
      })
    ];
    envSources = [ packages.melts.lib ];
  };
  template = path "/makes/applications/forces/infra-apply/entrypoint.sh";
}
