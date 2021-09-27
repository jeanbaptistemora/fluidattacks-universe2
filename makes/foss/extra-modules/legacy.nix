{ inputs
, projectPath
, ...
}:
{
  config = {
    inputs = {
      legacy = {
        path = rel:
          /. + (builtins.unsafeDiscardStringContext (projectPath "/")) + rel;
        importUtility = utility:
          import (projectPath "/makes/utils/${utility}")
            inputs.legacy.path
            inputs.nixpkgs;
      };
    };

    outputs = inputs.nixpkgs.lib.attrsets.mapAttrs'
      (name: value: {
        name = "/legacy/${name}";
        inherit value;
      })
      (inputs.product);
  };
}
