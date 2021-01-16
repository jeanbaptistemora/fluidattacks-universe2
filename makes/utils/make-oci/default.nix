# Create an OCI image with sensible defaults
# https://grahamc.com/blog/nix-and-layered-docker-images
# https://github.com/moby/moby/blob/master/image/spec/v1.2.md#image-json-field-descriptions

pkgs:

{ config ? null
, contents
, extraCommands ? null
, name
}:

pkgs.dockerTools.buildLayeredImage {
  inherit config;
  inherit contents;
  created = null;
  inherit extraCommands;
  maxLayers = 125;
  inherit name;
  tag = "oci";
}
