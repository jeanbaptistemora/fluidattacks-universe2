let
  pkgs = import ../../../../../pkgs/stable.nix;
in
  pkgs.dockerTools.pullImage {
    finalImageName = "nixos";
    finalImageTag = "nix";

    imageName = "nixos/nix";
    imageDigest = "sha256:af330838e838cedea2355e7ca267280fc9dd68615888f4e20972ec51beb101d8";

    sha256 = "1vynf6w0alx39h75s0a33lcif49j2h9vdhh04ci4aqzyd1jj7hf3";
  }
