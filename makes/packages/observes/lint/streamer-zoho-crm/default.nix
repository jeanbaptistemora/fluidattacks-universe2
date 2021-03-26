{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-lint-streamer-zoho-crm";
  arguments = {
    envSrc = path "/observes/singer/streamer_zoho_crm";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.linter
      packages.observes.env.development.streamer-zoho-crm
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/lint_builder.sh";
}
