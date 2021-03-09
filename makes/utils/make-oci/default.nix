# Create an OCI image with sensible defaults
# https://grahamc.com/blog/nix-and-layered-docker-images
# https://github.com/moby/moby/blob/master/image/spec/v1.2.md#image-json-field-descriptions

_: pkgs:

{ config ? null
, contents ? [ ]
, extraCommands ? ""
}:

pkgs.dockerTools.buildLayeredImage {
  inherit config;
  inherit contents;
  created = "1970-01-01T00:00:01Z";
  inherit extraCommands;
  maxLayers = 125;
  name = "oci";
  tag = "latest";
}
