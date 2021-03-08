{ makeDerivation
, packages
, path
, ...
}:
makeDerivation {
  arguments = {
    envSrcSkimsSkims = path "/skims/skims";
  };
  builder = path "/makes/packages/skims/security/builder.sh";
  name = "skims-security";
  searchPaths = {
    envSources = [ packages.skims.config-development ];
  };
}
