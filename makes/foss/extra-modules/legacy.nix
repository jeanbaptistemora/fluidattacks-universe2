{ inputs
, ...
}:
{
  config = {
    outputs = inputs.nixpkgs.lib.attrsets.mapAttrs'
      (name: value: {
        name = "/legacy/${name}";
        inherit value;
      })
      (inputs.product);
  };
}
