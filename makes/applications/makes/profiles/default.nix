{ makesPkgs
, path
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path makesPkgs;
  makeTemplate = import (path "/makes/utils/make-template") path makesPkgs;
in
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
      envIntegratesCache = [ "integrates-cache" ];
      envIntegratesDb = [ "integrates-db" ];
      envIntegratesStorage = [ "integrates-storage" ];
      envForces = [ "forces" ];
      envHacker = [ "melts-vpn" "melts" "sorts" "skims" ];
      envMelts = [ "melts" ];
      envReviews = [ "reviews" ];
      envSkims = [ "skims" ];
      envSorts = [ "sorts" ];
    };
  name = "makes-profiles";
  template = path "/makes/applications/makes/profiles/entrypoint.sh";
}
