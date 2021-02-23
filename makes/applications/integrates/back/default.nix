{ integratesPkgs
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint integratesPkgs {
  arguments = {
    envCertsDevelopment = packages.integrates.back.certs.development;
    envIntegratesEnv = packages.integrates.back.env;
  };
  name = "integrates-back";
  searchPaths = {
    envPaths = [
      packages.makes.done
      packages.makes.kill-port
      packages.makes.wait
    ];
  };
  template = path "/makes/applications/integrates/back/entrypoint.sh";
}
