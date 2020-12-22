# Create an OCI image with sensible defaults
# https://github.com/moby/moby/blob/master/image/spec/v1.2.md#image-json-field-descriptions

pkgs:

{
  config,
  contents,
  extraCommands,
  name,
  tag,
}:

pkgs.dockerTools.buildLayeredImage (attrs // {
  config = config;
  contents = contents;
  created = null;
  extraCommands = extraCommands;
  maxLayers = 125;
  name = name;
  tag = tag;
})
