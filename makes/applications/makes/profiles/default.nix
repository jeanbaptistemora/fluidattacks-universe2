{ makeEntrypoint
, makeTemplate
, path
, ...
}:
makeEntrypoint {
  arguments = builtins.mapAttrs
    (_: envPackages: makeTemplate {
      arguments = { inherit envPackages; };
      name = "makes-profile-template";
      template = path "/makes/applications/makes/profiles/template.sh";
    })
    {
      envIntegratesBack = [
        "integrates-back"
        "integrates-back-probes-liveness"
        "integrates-back-probes-readiness"
      ];
      envSkims = [ "skims" ];
    };
  name = "makes-profiles";
  template = path "/makes/applications/makes/profiles/entrypoint.sh";
}
