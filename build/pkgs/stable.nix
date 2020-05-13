let
  src = import ./stable-src.nix;
in
  import src {
    config.android_sdk.accept_license = true;
  }
