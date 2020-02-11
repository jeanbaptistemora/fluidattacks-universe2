pkgs:

pkgs.dockerTools.pullImage {
  finalImageName = "nix";
  finalImageTag = "2.3";

  imageName = "nixos/nix";
  imageDigest = "sha256:af330838e838cedea2355e7ca267280fc9dd68615888f4e20972ec51beb101d8";

  sha256 = "06sb57h1j20l69k5ypw2bd5amz23braisrjn7q6kad35bl6xpw82";
}
