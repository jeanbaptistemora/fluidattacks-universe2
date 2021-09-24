{ inputs
, projectPath
, ...
}:
{
  config = {
    inputs = {
      legacy = {
        importUtility = utility:
          import (projectPath "/makes/utils/${utility}")
            (path: /. + (builtins.unsafeDiscardStringContext (projectPath "/")) + path)
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
